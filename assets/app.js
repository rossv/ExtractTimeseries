let pyodideReady = null;
let currentOutfilePath = null;
let availableIds = [];
let availableParams = [];
let filteredIds = [];
let filteredParams = [];

const statusArea = document.getElementById('statusArea');
const fileStatus = document.getElementById('fileStatus');
const idsList = document.getElementById('idsList');
const paramsList = document.getElementById('paramsList');
const elementTypeSelect = document.getElementById('elementType');
const idFilterInput = document.getElementById('idFilter');
const paramFilterInput = document.getElementById('paramFilter');
const extractBtn = document.getElementById('extractBtn');
const runSummary = document.getElementById('runSummary');
const progressBar = document.getElementById('progressBar');
const downloadArea = document.getElementById('downloadArea');

function setStatus(message, type = 'info') {
  statusArea.textContent = message;
  statusArea.dataset.type = type;
}

async function loadPyodideAndPackages() {
  const pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.3/full/' });
  setStatus('Loading Python packages (pandas, swmmtoolbox)...');
  await pyodide.loadPackage(['pandas']);
  const micropip = await pyodide.pyimport('micropip');
  await micropip.install('swmmtoolbox==1.2.0');

  const coreCode = await (await fetch('./core.py')).text();
  await pyodide.runPythonAsync(coreCode);
  const webSupport = await (await fetch('./web_support.py')).text();
  await pyodide.runPythonAsync(webSupport);

  return pyodide;
}

function ensurePyodideReady() {
  if (!pyodideReady) {
    pyodideReady = loadPyodideAndPackages().catch((err) => {
      setStatus('Failed to load Pyodide or dependencies. Check your connection and refresh.', 'error');
      console.error(err);
    });
  }
  return pyodideReady;
}

async function handleFileSelect(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  setStatus('Preparing Pyodide runtime...');
  const pyodide = await ensurePyodideReady();
  if (!pyodide) return;

  const arrayBuffer = await file.arrayBuffer();
  pyodide.FS.mkdirTree('/data');
  currentOutfilePath = `/data/${sanitizeFilename(file.name) || 'swmm.out'}`;
  pyodide.FS.writeFile(currentOutfilePath, new Uint8Array(arrayBuffer));

  fileStatus.textContent = `Loaded ${file.name} (${formatBytes(file.size)})`;
  setStatus('File stored in memory. Discovering IDs and parameters...');
  await refreshLists();
}

function sanitizeFilename(name) {
  return name.replace(/[^a-zA-Z0-9._-]/g, '_');
}

function formatBytes(bytes) {
  if (!bytes) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let idx = 0;
  while (size >= 1024 && idx < units.length - 1) {
    size /= 1024;
    idx += 1;
  }
  return `${size.toFixed(2)} ${units[idx]}`;
}

function renderList(container, items, name) {
  container.innerHTML = '';
  if (!items.length) {
    container.textContent = `No ${name} available.`;
    return;
  }
  items.forEach((item) => {
    const id = `${name}-${item}`;
    const label = document.createElement('label');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = item;
    checkbox.name = `${name}Item`;
    checkbox.id = id;
    checkbox.addEventListener('change', updateSummary);
    const span = document.createElement('span');
    span.textContent = item;
    label.appendChild(checkbox);
    label.appendChild(span);
    container.appendChild(label);
  });
}

function filterLists() {
  const idFilter = idFilterInput.value.toLowerCase();
  const paramFilter = paramFilterInput.value.toLowerCase();
  filteredIds = availableIds.filter((i) => i.toLowerCase().includes(idFilter));
  filteredParams = availableParams.filter((p) => p.toLowerCase().includes(paramFilter));
  renderList(idsList, filteredIds, 'id');
  renderList(paramsList, filteredParams, 'param');
  updateSummary();
}

async function refreshLists() {
  if (!currentOutfilePath) return;
  const pyodide = await ensurePyodideReady();
  const elementType = elementTypeSelect.value;

  try {
    const code = `\nfrom web_support import list_ids_js, list_params_js\nids = list_ids_js('${currentOutfilePath}', '${elementType}')\nparams = list_params_js('${currentOutfilePath}', '${elementType}')\n`;
    await pyodide.runPythonAsync(code);
    availableIds = pyodide.globals.get('ids').toJs();
    availableParams = pyodide.globals.get('params').toJs();
    setStatus(`Found ${availableIds.length} IDs and ${availableParams.length} parameters for ${elementType}.`);
    filterLists();
    extractBtn.disabled = !availableIds.length || !availableParams.length;
  } catch (err) {
    console.error(err);
    setStatus('Could not read IDs/parameters from this file. Make sure it is a valid SWMM .out.', 'error');
  }
}

function getSelectedValues(name) {
  return Array.from(document.querySelectorAll(`input[name="${name}Item"]:checked`)).map((el) => el.value);
}

function updateSummary() {
  const ids = getSelectedValues('id');
  const params = getSelectedValues('param');
  runSummary.textContent = `Selected ${ids.length} IDs × ${params.length} parameters.`;
  extractBtn.disabled = !ids.length || !params.length;
}

async function handleExtract() {
  const ids = getSelectedValues('id');
  const params = getSelectedValues('param');
  if (!ids.length || !params.length || !currentOutfilePath) return;

  const pyodide = await ensurePyodideReady();
  setStatus('Running extraction inside the browser...');
  progressBar.style.width = '5%';
  downloadArea.innerHTML = '';

  const flowUnit = document.getElementById('flowUnit').value;
  const lenUnit = document.getElementById('lengthUnit').value;
  const velUnit = document.getElementById('velocityUnit').value;
  const outputFormat = document.getElementById('outputFormat').value;

  const payload = {
    outfile: currentOutfilePath,
    element_type: elementTypeSelect.value,
    ids,
    params,
    units: { flow: flowUnit, length: lenUnit, velocity: velUnit },
    output_format: outputFormat,
  };

  try {
    pyodide.globals.set('payload', payload);
    const pyCode = `\nfrom web_support import extract_to_text\nresult = extract_to_text(**payload)`;
    await pyodide.runPythonAsync(pyCode);
    const pyResult = pyodide.globals.get('result').toJs({ create_pyproxies: false });
    const files = Object.entries(pyResult); // [[filename, content], ...]

    const total = files.length;
    let completed = 0;
    files.forEach(([filename, content]) => {
      const blob = new Blob([content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const card = document.createElement('div');
      card.className = 'download-card';
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.textContent = filename;
      card.appendChild(link);
      downloadArea.appendChild(card);
      completed += 1;
      progressBar.style.width = `${Math.round((completed / total) * 100)}%`;
    });

    setStatus(`Extraction complete: ${files.length} file(s) ready.`);
    progressBar.style.width = '100%';
  } catch (err) {
    console.error(err);
    setStatus('Extraction failed. See console for details.', 'error');
    progressBar.style.width = '0%';
  }
}

// Wire up events
document.getElementById('outFile').addEventListener('change', handleFileSelect);
elementTypeSelect.addEventListener('change', refreshLists);
idFilterInput.addEventListener('input', filterLists);
paramFilterInput.addEventListener('input', filterLists);
extractBtn.addEventListener('click', handleExtract);

updateSummary();
