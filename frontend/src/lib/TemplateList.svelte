<script>
  import { onMount, createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  const API_URL = 'http://localhost:8001';

  let templates = [];
  let loading = true;
  let errorMessage = '';

  onMount(async () => {
    await loadTemplates();
  });

  async function loadTemplates() {
    loading = true;
    errorMessage = '';

    try {
      const response = await fetch(`${API_URL}/api/templates/`);
      const result = await response.json();

      if (response.ok && result.success) {
        templates = result.data;
      } else {
        errorMessage = '템플릿 목록을 불러올 수 없습니다.';
      }
    } catch (error) {
      errorMessage = '서버와 통신할 수 없습니다.';
    } finally {
      loading = false;
    }
  }

  async function deleteTemplate(templateId) {
    if (!confirm('정말 이 템플릿을 삭제하시겠습니까?')) {
      return;
    }

    try {
      const response = await fetch(`${API_URL}/api/templates/${templateId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        await loadTemplates();
      } else {
        alert('템플릿 삭제에 실패했습니다.');
      }
    } catch (error) {
      alert('서버와 통신할 수 없습니다.');
    }
  }

  function selectTemplate(template) {
    dispatch('select', template);
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
</script>

<div class="template-list">
  <div class="header">
    <h2>템플릿 목록</h2>
    <button class="refresh-btn" on:click={loadTemplates}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M23 4v6h-6M1 20v-6h6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      새로고침
    </button>
  </div>

  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>
  {:else if errorMessage}
    <div class="error">
      {errorMessage}
    </div>
  {:else if templates.length === 0}
    <div class="empty">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <polyline points="13 2 13 9 20 9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <p>아직 업로드된 템플릿이 없습니다.</p>
      <p class="hint">템플릿 업로드 탭에서 파일을 업로드해주세요.</p>
    </div>
  {:else}
    <div class="grid">
      {#each templates as template (template.id)}
        <div class="template-card">
          <div class="card-header">
            <h3>{template.name}</h3>
            <span class="status" class:uploaded={template.status === 'uploaded'}>
              {template.status}
            </span>
          </div>

          {#if template.description}
            <p class="description">{template.description}</p>
          {/if}

          <div class="card-footer">
            <span class="date">{formatDate(template.created_at)}</span>
            <div class="actions">
              <button
                class="btn-use"
                on:click={() => selectTemplate(template)}
              >
                사용하기
              </button>
              <button
                class="btn-delete"
                on:click={() => deleteTemplate(template.id)}
              >
                삭제
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .template-list {
    max-width: 1000px;
    margin: 0 auto;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  h2 {
    color: #58a6ff;
    margin: 0;
    font-size: 1.5rem;
  }

  .refresh-btn {
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

  .refresh-btn:hover {
    background: #30363d;
    border-color: #58a6ff;
  }

  .loading,
  .error,
  .empty {
    text-align: center;
    padding: 3rem;
    color: #8b949e;
  }

  .loading .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #30363d;
    border-top: 3px solid #58a6ff;
    border-radius: 50%;
    margin: 0 auto 1rem;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .empty svg {
    color: #58a6ff;
    margin-bottom: 1rem;
  }

  .empty .hint {
    font-size: 0.9rem;
    color: #6e7681;
  }

  .error {
    color: #f85149;
    background: rgba(248, 81, 73, 0.1);
    border: 1px solid #f85149;
    border-radius: 6px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .template-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.5rem;
    transition: all 0.2s;
  }

  .template-card:hover {
    border-color: #58a6ff;
    box-shadow: 0 0 10px rgba(88, 166, 255, 0.1);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 1rem;
  }

  .card-header h3 {
    margin: 0;
    color: #c9d1d9;
    font-size: 1.1rem;
    flex: 1;
  }

  .status {
    padding: 0.25rem 0.75rem;
    background: #21262d;
    color: #8b949e;
    border-radius: 12px;
    font-size: 0.75rem;
    text-transform: uppercase;
  }

  .status.uploaded {
    background: rgba(63, 185, 80, 0.1);
    color: #3fb950;
  }

  .description {
    color: #8b949e;
    margin: 0 0 1rem 0;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #30363d;
  }

  .date {
    color: #6e7681;
    font-size: 0.8rem;
  }

  .actions {
    display: flex;
    gap: 0.5rem;
  }

  .actions button {
    padding: 0.5rem 1rem;
    border: 1px solid #30363d;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.2s;
  }

  .btn-use {
    background: #1f6feb;
    color: white;
    border-color: #1f6feb;
  }

  .btn-use:hover {
    background: #388bfd;
  }

  .btn-delete {
    background: transparent;
    color: #f85149;
    border-color: #f85149;
  }

  .btn-delete:hover {
    background: rgba(248, 81, 73, 0.1);
  }
</style>
