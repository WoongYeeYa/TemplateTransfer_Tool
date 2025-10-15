<script>
  import { createEventDispatcher } from 'svelte';

  export let template;

  const dispatch = createEventDispatcher();
  const API_URL = 'http://localhost:8001';

  let filename = '';
  let isGenerating = false;
  let errorMessage = '';
  let successMessage = '';

  async function generateHwp() {
    isGenerating = true;
    errorMessage = '';
    successMessage = '';

    // 제목이 없으면 템플릿 이름 사용
    const finalFilename = filename.trim() || template.name;

    try {
      const response = await fetch(`${API_URL}/api/hwp/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          template_id: template.id,
          filename: finalFilename
        })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        if (result.file_url) {
          // 파일 다운로드
          const link = document.createElement('a');
          link.href = result.file_url;
          link.download = result.filename || `${finalFilename}.hwp`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);

          successMessage = 'HWP 파일이 생성되어 다운로드되었습니다!';
        } else {
          successMessage = result.message || 'HWP 파일 생성 요청이 완료되었습니다.';
        }
      } else {
        // 상세한 에러 정보 표시
        console.error('HWP Generation Error:', result);
        if (result.detail) {
          errorMessage = `검증 오류: ${JSON.stringify(result.detail)}`;
        } else {
          errorMessage = result.message || result.detail || 'HWP 생성에 실패했습니다.';
        }
      }
    } catch (error) {
      errorMessage = '서버와 통신할 수 없습니다.';
    } finally {
      isGenerating = false;
    }
  }

  function goBack() {
    dispatch('back');
  }
</script>

<div class="hwp-generator">
  <div class="header">
    <button class="back-btn" on:click={goBack}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <line x1="19" y1="12" x2="5" y2="12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <polyline points="12 19 5 12 12 5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      돌아가기
    </button>
    <h2>HWP 파일 생성</h2>
  </div>

  <div class="template-info">
    <h3>템플릿: {template.name}</h3>
    {#if template.description}
      <p>{template.description}</p>
    {/if}
  </div>

  <form on:submit|preventDefault={generateHwp}>
    <div class="field-group">
      <label for="filename">
        파일 제목 <span class="optional">(선택사항)</span>
      </label>
      <input
        type="text"
        id="filename"
        bind:value={filename}
        placeholder={template.name}
        disabled={isGenerating}
      />
      <p class="hint">
        제목을 입력하지 않으면 템플릿 이름("<strong>{template.name}</strong>")으로 생성됩니다.
      </p>
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

    <div class="actions">
      <button
        type="submit"
        class="btn-generate"
        disabled={isGenerating}
      >
        {#if isGenerating}
          <div class="spinner-small"></div>
          생성 중...
        {:else}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="7 10 12 15 17 10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="15" x2="12" y2="3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          HWP 파일 생성
        {/if}
      </button>
    </div>
  </form>
</div>

<style>
  .hwp-generator {
    max-width: 700px;
    margin: 0 auto;
  }

  .header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .back-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .back-btn:hover {
    background: #30363d;
    border-color: #58a6ff;
  }

  h2 {
    color: #58a6ff;
    margin: 0;
    font-size: 1.5rem;
  }

  .template-info {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }

  .template-info h3 {
    margin: 0 0 0.5rem 0;
    color: #c9d1d9;
    font-size: 1.2rem;
  }

  .template-info p {
    margin: 0;
    color: #8b949e;
  }

  .field-group {
    margin-bottom: 2rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #c9d1d9;
    font-weight: 500;
  }

  .optional {
    color: #8b949e;
    font-weight: 400;
    font-size: 0.9rem;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #c9d1d9;
    font-size: 1rem;
    font-family: inherit;
    box-sizing: border-box;
  }

  input:focus {
    outline: none;
    border-color: #58a6ff;
  }

  input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .hint {
    margin: 0.5rem 0 0 0;
    color: #8b949e;
    font-size: 0.9rem;
  }

  .hint strong {
    color: #58a6ff;
  }

  .message {
    margin-bottom: 1.5rem;
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

  .actions {
    display: flex;
    justify-content: center;
  }

  .btn-generate {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 2rem;
    background: #1f6feb;
    color: white;
    border: 1px solid #1f6feb;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 500;
    transition: all 0.2s;
  }

  .btn-generate:hover:not(:disabled) {
    background: #388bfd;
  }

  .btn-generate:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .spinner-small {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
