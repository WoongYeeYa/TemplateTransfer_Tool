<script>
  import { onMount } from 'svelte';
  import TemplateUpload from './lib/TemplateUpload.svelte';
  import TemplateList from './lib/TemplateList.svelte';
  import HwpGenerator from './lib/HwpGenerator.svelte';

  let currentView = 'upload'; // 'upload', 'list', 'generate'
  let selectedTemplate = null;

  function handleTemplateUploaded() {
    currentView = 'list';
  }

  function handleTemplateSelected(template) {
    selectedTemplate = template;
    currentView = 'generate';
  }
</script>

<main>
  <div class="container">
    <header>
      <h1>템플릿 관리 시스템</h1>
      <p>워드/한글 파일 양식 자동화</p>
    </header>

    <nav>
      <button
        class:active={currentView === 'upload'}
        on:click={() => currentView = 'upload'}
      >
        템플릿 업로드
      </button>
      <button
        class:active={currentView === 'list'}
        on:click={() => currentView = 'list'}
      >
        템플릿 목록
      </button>
    </nav>

    <div class="content">
      {#if currentView === 'upload'}
        <TemplateUpload on:uploaded={handleTemplateUploaded} />
      {:else if currentView === 'list'}
        <TemplateList on:select={(e) => handleTemplateSelected(e.detail)} />
      {:else if currentView === 'generate'}
        <HwpGenerator template={selectedTemplate} on:back={() => currentView = 'list'} />
      {/if}
    </div>
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background: #0d1117;
    color: #c9d1d9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
  }

  main {
    min-height: 100vh;
    padding: 2rem;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
  }

  header {
    text-align: center;
    margin-bottom: 3rem;
    padding: 2rem 0;
    border-bottom: 1px solid #30363d;
  }

  h1 {
    font-size: 2.5rem;
    margin: 0 0 0.5rem 0;
    color: #58a6ff;
    font-weight: 600;
  }

  header p {
    color: #8b949e;
    font-size: 1.1rem;
    margin: 0;
  }

  nav {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    padding: 1rem;
    background: #161b22;
    border-radius: 8px;
    border: 1px solid #30363d;
  }

  nav button {
    flex: 1;
    padding: 0.75rem 1.5rem;
    background: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s;
  }

  nav button:hover {
    background: #30363d;
    border-color: #58a6ff;
  }

  nav button.active {
    background: #1f6feb;
    color: white;
    border-color: #1f6feb;
  }

  .content {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 2rem;
    min-height: 400px;
  }
</style>
