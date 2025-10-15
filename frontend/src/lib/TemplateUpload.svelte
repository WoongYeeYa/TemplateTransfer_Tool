<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  const API_URL = 'http://localhost:8001';

  let isDragging = false;
  let isUploading = false;
  let uploadProgress = 0;
  let fileName = '';
  let errorMessage = '';
  let successMessage = '';

  function handleDragOver(e) {
    e.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  async function handleDrop(e) {
    e.preventDefault();
    isDragging = false;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
  }

  async function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
  }

  async function uploadFile(file) {
    fileName = file.name;

    // 파일 확장자 검증
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['docx', 'hwp', 'doc'].includes(ext)) {
      errorMessage = '지원하지 않는 파일 형식입니다. .docx 또는 .hwp 파일만 업로드 가능합니다.';
      return;
    }

    isUploading = true;
    errorMessage = '';
    successMessage = '';

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/api/templates/upload`, {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (response.ok && result.success) {
        successMessage = '파일이 성공적으로 업로드되었습니다!';
        uploadProgress = 100;

        // 초기화
        setTimeout(() => {
          fileName = '';
          uploadProgress = 0;
          isUploading = false;

          dispatch('uploaded', result.data);
        }, 1500);
      } else {
        errorMessage = result.detail || '업로드에 실패했습니다.';
        isUploading = false;
      }
    } catch (error) {
      errorMessage = '서버와 통신할 수 없습니다. 백엔드 서버가 실행 중인지 확인하세요.';
      isUploading = false;
    }
  }
</script>

<div class="upload-container">
  <h2>템플릿 파일 업로드</h2>
  <p class="info">파일을 업로드하면 자동으로 분석됩니다</p>

  <div
    class="drop-zone"
    class:dragging={isDragging}
    class:uploading={isUploading}
    on:dragover={handleDragOver}
    on:dragleave={handleDragLeave}
    on:drop={handleDrop}
  >
    {#if isUploading}
      <div class="upload-status">
        <div class="spinner"></div>
        <p>업로드 중...</p>
        {#if fileName}
          <p class="file-name">{fileName}</p>
        {/if}
      </div>
    {:else}
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <polyline points="17 8 12 3 7 8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <line x1="12" y1="3" x2="12" y2="15" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <p>파일을 드래그 앤 드롭하거나 클릭하여 선택하세요</p>
      <p class="file-types">.docx, .hwp 파일 지원</p>
      <input
        type="file"
        accept=".docx,.hwp,.doc"
        on:change={handleFileSelect}
        disabled={isUploading}
      />
    {/if}
  </div>

  {#if errorMessage}
    <div class="message error">
      {errorMessage}
    </div>
  {/if}

  {#if successMessage}
    <div class="message success">
      {successMessage}
    </div>
  {/if}
</div>

<style>
  .upload-container {
    max-width: 600px;
    margin: 0 auto;
  }

  h2 {
    color: #58a6ff;
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
  }

  .info {
    color: #8b949e;
    margin-bottom: 2rem;
    font-size: 0.95rem;
  }

  .drop-zone {
    border: 2px dashed #30363d;
    border-radius: 8px;
    padding: 3rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    position: relative;
  }

  .drop-zone:hover {
    border-color: #58a6ff;
    background: rgba(88, 166, 255, 0.05);
  }

  .drop-zone.dragging {
    border-color: #58a6ff;
    background: rgba(88, 166, 255, 0.1);
  }

  .drop-zone.uploading {
    border-style: solid;
    cursor: default;
  }

  .drop-zone svg {
    color: #58a6ff;
    margin-bottom: 1rem;
  }

  .drop-zone p {
    margin: 0.5rem 0;
    color: #c9d1d9;
  }

  .drop-zone .file-types {
    color: #8b949e;
    font-size: 0.9rem;
  }

  .drop-zone input[type="file"] {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
  }

  .upload-status {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #30363d;
    border-top: 3px solid #58a6ff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .file-name {
    font-size: 0.9rem;
    color: #8b949e;
  }

  .message {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 6px;
    font-weight: 500;
  }

  .message.error {
    background: rgba(248, 81, 73, 0.1);
    border: 1px solid #f85149;
    color: #f85149;
  }

  .message.success {
    background: rgba(63, 185, 80, 0.1);
    border: 1px solid #3fb950;
    color: #3fb950;
  }
</style>
