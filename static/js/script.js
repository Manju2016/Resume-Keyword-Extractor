
/* Resume Keyword Extractor: vanilla JS for index.html and results.html */
(() => {
    'use strict';

    /* ---------- Configuration ---------- */
    const CONFIG = {
        BACKEND_ENABLED: true,
        EXTRACT_URL: '/extract',
        DOWNLOAD_URL: '/download',
        RESULTS_URL: '/results',
        MAX_BYTES: 10 * 1024 * 1024,
        ALLOWED_EXT: ['pdf', 'docx', 'txt']
    };

    const $ = (id) => document.getElementById(id);

    let selectedFile = null;
    let isSubmitting = false;

    /* ---------- Shared helpers ---------- */

    function formatFileSize(bytes) {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) {
            return `${(bytes / 1024).toFixed(1)} KB`;
        }
        return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    }

    const getExtension = (name) =>
        name.includes('.') ? name.split('.').pop().toLowerCase() : '';

    function showMessage(element, text, type = 'error') {
        if (!element) return;
        element.textContent = text;
        element.className = `alert ${type}`;
        element.hidden = false;
    }

    function clearMessage(element) {
        if (!element) return;
        element.hidden = true;
        element.textContent = '';
    }

    const refreshIcons = () => {
        if (window.lucide) window.lucide.createIcons();
    };

    /* ---------- Navigation ---------- */

    function setupNavigation() {
        const toggle = $('navToggle');
        const menu = $('navMenu');

        if (toggle && menu) {
            toggle.addEventListener('click', () => {
                const open = menu.classList.toggle('open');
                toggle.setAttribute('aria-expanded', String(open));
            });

            menu.addEventListener('click', (event) => {
                if (event.target.closest('a')) {
                    menu.classList.remove('open');
                    toggle.setAttribute('aria-expanded', 'false');
                }
            });
        }

        const year = $('year');
        if (year) year.textContent = new Date().getFullYear();
    }

    /* ---------- File validation ---------- */

    function validateFile(file) {
        if (!CONFIG.ALLOWED_EXT.includes(getExtension(file.name))) {
            return 'Unsupported file type. Upload a PDF, DOCX, or TXT file.';
        }

        if (file.size === 0) {
            return 'This file is empty. Choose a resume containing text.';
        }

        if (file.size > CONFIG.MAX_BYTES) {
            return `This file is ${formatFileSize(file.size)}. The maximum size is 10 MB.`;
        }

        return null;
    }

    function handleFileSelection(file) {
        const message = $('uploadMessage');
        clearMessage(message);

        if (!file) return;

        const error = validateFile(file);

        if (error) {
            removeSelectedFile(false);
            showMessage(message, error);
            return;
        }

        selectedFile = file;
        renderSelectedFile(file);
    }

    function renderSelectedFile(file) {
        $('fileName').textContent = file.name;
        $('fileExt').textContent = getExtension(file.name).toUpperCase();
        $('fileSize').textContent = formatFileSize(file.size);
        $('fileInfo').hidden = false;
        $('extractBtn').disabled = false;
    }

    function removeSelectedFile(clearInput = true) {
        selectedFile = null;

        if (clearInput) $('resumeInput').value = '';

        $('fileInfo').hidden = true;
        $('extractBtn').disabled = true;
        clearMessage($('uploadMessage'));
    }

    function setLoading(loading) {
        isSubmitting = loading;

        const button = $('extractBtn');
        button.disabled = loading || !selectedFile;
        button.setAttribute('aria-busy', String(loading));

        const spinner = button.querySelector('.spinner');
        if (spinner) spinner.hidden = !loading;

        $('extractLabel').textContent = loading
            ? 'Processing…'
            : 'Extract Details';
    }

    /* ---------- Resume upload and extraction ---------- */

    async function submitResume(event) {
        event.preventDefault();

        if (isSubmitting || !selectedFile) return;

        const message = $('uploadMessage');
        clearMessage(message);
        setLoading(true);

        if (!CONFIG.BACKEND_ENABLED) {
            setLoading(false);
            showMessage(
                message,
                'The extraction service is not connected.',
                'warning'
            );
            return;
        }

        try {
            const body = new FormData();
            body.append('resume', selectedFile);

            const response = await fetch(CONFIG.EXTRACT_URL, {
                method: 'POST',
                body
            });

            let data = null;

            try {
                data = await response.json();
            } catch (_) {
                // The server did not return JSON.
            }

            if (!response.ok) {
                throw new Error(
                    (data && data.error) ||
                    `The server returned an error (${response.status}).`
                );
            }

            if (!data || data.success !== true) {
                throw new Error(
                    (data && data.error) ||
                    'The resume could not be processed.'
                );
            }

            // Flask returns the results URL, including its unique key.
            window.location.href = data.redirect || CONFIG.RESULTS_URL;

        } catch (error) {
            const messageText = error instanceof TypeError
                ? 'Could not reach the server. Check that Flask is running.'
                : error.message;

            showMessage(message, messageText);
            setLoading(false);
        }
    }

    function setupUploadPage() {
        const input = $('resumeInput');
        const zone = $('dropzone');

        if (!input || !zone) return;

        input.addEventListener('change', () => {
            handleFileSelection(input.files[0]);
        });

        $('removeFile').addEventListener('click', () => {
            removeSelectedFile();
        });

        $('uploadForm').addEventListener('submit', submitResume);

        zone.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                input.click();
            }
        });

        ['dragenter', 'dragover'].forEach((name) => {
            zone.addEventListener(name, (event) => {
                event.preventDefault();
                zone.classList.add('is-dragover');
            });
        });

        ['dragleave', 'drop'].forEach((name) => {
            zone.addEventListener(name, (event) => {
                event.preventDefault();
                zone.classList.remove('is-dragover');
            });
        });

        zone.addEventListener('drop', (event) => {
            const files = event.dataTransfer.files;

            if (files.length > 1) {
                showMessage(
                    $('uploadMessage'),
                    'Drop one file at a time.'
                );
                return;
            }

            if (files[0]) {
                try {
                    const transfer = new DataTransfer();
                    transfer.items.add(files[0]);
                    input.files = transfer.files;
                } catch (_) {
                    // Some browsers do not support DataTransfer assignment.
                }

                handleFileSelection(files[0]);
            }
        });
    }

    /* ---------- Results rendering ---------- */

    const el = (tag, className, text) => {
        const node = document.createElement(tag);

        if (className) node.className = className;
        if (text !== undefined) node.textContent = String(text);

        return node;
    };

    function renderEmptyList(container, message) {
        if (!container) return;
        container.replaceChildren(el('p', 'empty-inline', message));
    }

    function renderSkills(skills = {}, unverified = []) {
        const list = $('skillsList');
        if (!list) return;

        list.replaceChildren();

        const categories = Object.entries(skills || {})
            .filter(([, items]) => Array.isArray(items) && items.length);

        categories.forEach(([name, items]) => {
            const section = el('div', 'category');
            const heading = el('h3', '', name);
            heading.append(el('span', 'count', String(items.length)));

            const tags = el('div', 'tags');

            items.forEach((skill) => {
                tags.append(el('span', 'tag tag-verified', skill));
            });

            section.append(heading, tags);
            list.append(section);
        });

        if (unverified.length) {
            const section = el('div', 'category');
            const heading = el('h3', '', 'Unverified candidates');
            heading.append(el('span', 'count', String(unverified.length)));

            const tags = el('div', 'tags');

            unverified.forEach((skill) => {
                tags.append(el('span', 'tag tag-unverified', skill));
            });

            section.append(heading, tags);
            list.append(section);
        }

        if (!categories.length && !unverified.length) {
            renderEmptyList(list, 'No skills were identified in this resume.');
        }
    }

    function renderEducation(items = []) {
        const box = $('eduList');
        if (!box) return;

        if (!Array.isArray(items) || !items.length) {
            renderEmptyList(box, 'No education details were identified.');
            return;
        }

        box.replaceChildren();

        items.forEach((item) => {
            const wrap = el('div', 'edu-item');
            const details = el('dl');

            [
                ['Degree or qualification', item.degree],
                ['Institution', item.institution],
                ['Graduation year', item.year],
                ['Other details', item.details]
            ].forEach(([label, value]) => {
                details.append(
                    el('dt', '', label),
                    value
                        ? el('dd', '', value)
                        : el('dd', 'missing', 'Not found in resume')
                );
            });

            wrap.append(details);
            box.append(wrap);
        });
    }

    function renderCertifications(items = []) {
        const box = $('certList');
        if (!box) return;

        if (!Array.isArray(items) || !items.length) {
            renderEmptyList(
                box,
                'No certifications were identified in this resume.'
            );
            return;
        }

        const tags = el('div', 'tags');

        items.forEach((certification) => {
            tags.append(el('span', 'tag tag-verified', certification));
        });

        box.replaceChildren(tags);
    }

    function renderKeywords(items = []) {
        const box = $('kwList');
        if (!box) return;

        if (!Array.isArray(items) || !items.length) {
            renderEmptyList(box, 'No additional technical keywords were identified.');
            return;
        }

        const tags = el('div', 'tags');

        items.forEach((item) => {
            const keyword = typeof item === 'string'
                ? { term: item }
                : item;

            const tag = el('span', 'tag tag-verified', keyword.term || '');

            if (keyword.source) {
                tag.append(el('span', 'kw-source', ` · ${keyword.source}`));
            }

            tags.append(tag);
        });

        box.replaceChildren(tags);
    }

    function renderResults(data) {
        if ($('emptyState')) $('emptyState').hidden = true;
        if ($('resultsView')) $('resultsView').hidden = false;

        $('resultFile').textContent = data.filename || 'Uploaded resume';

        const status = $('resultStatus');
        status.textContent = data.status === 'complete'
            ? 'Analysis complete'
            : (data.status || 'Status unknown');

        status.classList.toggle('complete', data.status === 'complete');

        const skills = data.skills || {};
        const skillCount = Object.values(skills).reduce(
            (total, items) => total + (Array.isArray(items) ? items.length : 0),
            0
        );

        $('statSkills').textContent = skillCount;
        $('statQuals').textContent = (data.education || []).length;
        $('statCerts').textContent = (data.certifications || []).length;
        $('statKeywords').textContent = (data.keywords || []).length;

        renderSkills(skills, data.unverified || []);
        renderEducation(data.education || []);
        renderCertifications(data.certifications || []);
        renderKeywords(data.keywords || []);

        const resumeText = $('resumeText');
        if (resumeText) {
            resumeText.textContent = data.text || 'No text available.';
        }

        refreshIcons();
    }

    function renderEmptyState() {
        if ($('emptyState')) $('emptyState').hidden = false;
        if ($('resultsView')) $('resultsView').hidden = true;
    }

    /* ---------- Download report: FIXED ---------- */

    async function downloadResults(format = 'json') {
        const message = $('downloadMessage');
        clearMessage(message);

        if (!CONFIG.BACKEND_ENABLED) {
            showMessage(
                message,
                'Downloads are unavailable because the backend is disconnected.',
                'warning'
            );
            return;
        }

        // The key is generated by Flask after a successful upload.
        const params = new URLSearchParams(window.location.search);
        const key = params.get('key');

        if (!key) {
            showMessage(
                message,
                'Results key not found. Please upload your resume again.',
                'error'
            );
            return;
        }

        // Pass both required parameters to the Flask download route.
        const url = new URL(CONFIG.DOWNLOAD_URL, window.location.origin);
        url.searchParams.set('format', format);
        url.searchParams.set('key', key);

        window.location.href = url.toString();
    }

    function setupResultsPage() {
        const data = window.RESULTS_DATA;

        if (data && typeof data === 'object') {
            renderResults(data);
        } else {
            renderEmptyState();
        }

        const downloadButton = $('downloadBtn');

        if (downloadButton) {
            downloadButton.addEventListener('click', () => {
                downloadResults('json');
            });
        }

        // Optional CSV button, if you add one to results.html.
        const csvButton = $('downloadCsvBtn');

        if (csvButton) {
            csvButton.addEventListener('click', () => {
                downloadResults('csv');
            });
        }
    }

    /* ---------- Initialize ---------- */

    document.addEventListener('DOMContentLoaded', () => {
        setupNavigation();

        const page = document.body.dataset.page;

        if (page === 'home') setupUploadPage();
        if (page === 'results') setupResultsPage();

        window.addEventListener('load', refreshIcons);
        refreshIcons();
    });
})();

