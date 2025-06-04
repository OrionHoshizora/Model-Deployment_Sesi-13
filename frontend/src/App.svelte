<script lang="ts">
  interface AbaloneData {
    sex: string;
    length: number;
    diameter: number;
    height: number;
    whole_weight: number;
    shucked_weight: number;
    viscera_weight: number;
    shell_weight: number;
  }

  let formData: AbaloneData = {
    sex: 'M',
    length: 0.595,
    diameter: 0.475,
    height: 0.15,
    whole_weight: 0.9145,
    shucked_weight: 0.3755,
    viscera_weight: 0.2055,
    shell_weight: 0.25
  };

  let predictionResult: any = null;
  let isLoading = false;
  let error = '';

  const sampleData = {
    adultMale: {
      sex: 'M',
      length: 0.595,
      diameter: 0.475,
      height: 0.15,
      whole_weight: 0.9145,
      shucked_weight: 0.3755,
      viscera_weight: 0.2055,
      shell_weight: 0.25
    },
    adultFemale: {
      sex: 'F',
      length: 0.53,
      diameter: 0.42,
      height: 0.135,
      whole_weight: 0.677,
      shucked_weight: 0.256,
      viscera_weight: 0.142,
      shell_weight: 0.21
    },
    infant: {
      sex: 'I',
      length: 0.2,
      diameter: 0.15,
      height: 0.03,
      whole_weight: 0.055,
      shucked_weight: 0.02,
      viscera_weight: 0.01,
      shell_weight: 0.015
    }
  };

  function loadSample(type: keyof typeof sampleData) {
    formData = { ...sampleData[type] };
    predictionResult = null;
    error = '';
  }

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  async function predictAge() {
    isLoading = true;
    error = '';
    predictionResult = null;

    try {
      console.log('Sending data:', formData);
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Received result:', result);
      predictionResult = result;
    } catch (err) {
      error = err instanceof Error ? err.message : 'An unknown error occurred';
      console.error('Prediction error:', err);
    } finally {
      isLoading = false;
    }
  }
</script>

<main>
  <div class="container">
    <header>
      <div class="header-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="12" cy="12" rx="10" ry="6" stroke="#000" stroke-width="2" fill="none"/>
          <ellipse cx="12" cy="12" rx="7" ry="4" stroke="#000" stroke-width="1.5" fill="none"/>
          <ellipse cx="12" cy="12" rx="4" ry="2" stroke="#000" stroke-width="1" fill="none"/>
        </svg>
      </div>
      <h1>Abalone Age Predictor</h1>
      <p>Prediksi umur abalone menggunakan model machine learning berdasarkan pengukuran fisik</p>
      <div class="student-info">
        <p>2702236156 - Veron Fujimori</p>
      </div>
    </header>

    <div class="content">
      <div class="samples">
        <h3>Sample Data</h3>
        <div class="sample-buttons">
          <button class="sample-btn male" on:click={() => loadSample('adultMale')}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="8" r="5" stroke="currentColor" stroke-width="2"/>
              <path d="M8 21v-3a5 5 0 0 1 10 0v3" stroke="currentColor" stroke-width="2"/>
              <path d="M16 4l4-4m0 0h-4m4 0v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Adult Male
          </button>
          <button class="sample-btn female" on:click={() => loadSample('adultFemale')}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="8" r="5" stroke="currentColor" stroke-width="2"/>
              <path d="M8 21v-3a5 5 0 0 1 10 0v3" stroke="currentColor" stroke-width="2"/>
              <circle cx="16" cy="4" r="2" stroke="currentColor" stroke-width="2"/>
              <path d="M16 6v6m-3-3h6" stroke="currentColor" stroke-width="2"/>
            </svg>
            Adult Female
          </button>
          <button class="sample-btn infant" on:click={() => loadSample('infant')}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2"/>
              <path d="M9 16h6c1 0 2 1 2 2v2c0 1-1 2-2 2H9c-1 0-2-1-2-2v-2c0-1 1-2 2-2z" stroke="currentColor" stroke-width="2"/>
              <path d="M12 2v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M8 4l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M16 4l-2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Infant
          </button>
        </div>
      </div>

      <form class="form" on:submit|preventDefault={predictAge}>
        <div class="form-grid">
          <div class="form-group">
            <label for="sex">Sex:</label>
            <select id="sex" bind:value={formData.sex}>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="I">Infant</option>
            </select>
          </div>

          <div class="form-group">
            <label for="length">Length:</label>
            <input id="length" type="number" step="any" bind:value={formData.length} />
          </div>

          <div class="form-group">
            <label for="diameter">Diameter:</label>
            <input id="diameter" type="number" step="any" bind:value={formData.diameter} />
          </div>

          <div class="form-group">
            <label for="height">Height:</label>
            <input id="height" type="number" step="any" bind:value={formData.height} />
          </div>

          <div class="form-group">
            <label for="whole_weight">Whole Weight:</label>
            <input id="whole_weight" type="number" step="any" bind:value={formData.whole_weight} />
          </div>

          <div class="form-group">
            <label for="shucked_weight">Shucked Weight:</label>
            <input id="shucked_weight" type="number" step="any" bind:value={formData.shucked_weight} />
          </div>

          <div class="form-group">
            <label for="viscera_weight">Viscera Weight:</label>
            <input id="viscera_weight" type="number" step="any" bind:value={formData.viscera_weight} />
          </div>

          <div class="form-group">
            <label for="shell_weight">Shell Weight:</label>
            <input id="shell_weight" type="number" step="any" bind:value={formData.shell_weight} />
          </div>
        </div>

        <button type="submit" class="predict-btn" disabled={isLoading}>
          {#if isLoading}
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="spinning">
              <path d="M12 6V2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M16.24 7.76L18.66 5.34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M18 12H22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M16.24 16.24L18.66 18.66" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M12 18V22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M7.76 16.24L5.34 18.66" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M6 12H2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M7.76 7.76L5.34 5.34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Analyzing...
          {:else}
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            </svg>
            Predict Age
          {/if}
        </button>
      </form>

      {#if error}
        <div class="error">
          <div class="error-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="#000" stroke-width="2" fill="none"/>
              <path d="M15 9l-6 6" stroke="#000" stroke-width="2" stroke-linecap="round"/>
              <path d="M9 9l6 6" stroke="#000" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <h3>Error</h3>
          </div>
          <p>{error}</p>
          <p><small>Make sure backend is running on {API_URL}</small></p>
        </div>
      {:else if predictionResult}
        <div class="result">
          <div class="result-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="#000" stroke-width="2" fill="none"/>
              <path d="M9 12l2 2 4-4" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3>Prediction Result</h3>
          </div>
          <div class="age-result">
            <div class="age-display">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="age-icon">
                <circle cx="12" cy="12" r="10" stroke="#000" stroke-width="2" fill="none"/>
                <path d="M12 6v6l4 2" stroke="#000" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <div class="age-info">
                <div class="age-number">{predictionResult.predicted_age?.toFixed(1) || 'N/A'}</div>
                <div class="age-label">years old</div>
              </div>
            </div>
          </div>
          
          {#if predictionResult.prediction_details}
            <div class="details">
              <div class="detail-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L2 7v10c0 5.55 3.84 9.74 9 11 5.16-1.26 9-5.45 9-11V7l-10-5z" stroke="currentColor" stroke-width="2" fill="none"/>
                </svg>
                <span><strong>Model:</strong> {predictionResult.prediction_details.model_type || 'Unknown'}</span>
              </div>
              <div class="detail-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3" stroke="currentColor" stroke-width="2" fill="none"/>
                  <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3" stroke="currentColor" stroke-width="2" fill="none"/>
                </svg>
                <span><strong>Features:</strong> {predictionResult.prediction_details.features_used || 'N/A'}</span>
              </div>
              {#if predictionResult.model_status}
                <div class="detail-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
                    <path d="M21 12h-6m-6 0H3" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <span><strong>Status:</strong> {predictionResult.model_status}</span>
                </div>
              {/if}
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: white;
    min-height: 100vh;
    color: #000;
  }

  .container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    padding: 30px;
    border: 1px solid #ddd;
  }

  header {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #ddd;
  }

  header h1 {
    margin: 0 0 10px 0;
    font-size: 2.5rem;
    color: #000;
  }

  header p {
    margin: 0;
    color: #666;
    font-size: 1.1rem;
  }

  .student-info {
    margin-top: 15px;
    padding: 10px 20px;
    background: #f9f9f9;
    border-radius: 6px;
    border: 1px solid #ddd;
    display: inline-block;
  }

  .student-info p {
    margin: 0;
    font-size: 0.95rem;
    color: #333;
    font-weight: 500;
  }

  .samples {
    margin-bottom: 30px;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 8px;
    border: 1px solid #eee;
  }

  .samples h3 {
    margin: 0 0 15px 0;
    color: #000;
  }

  .sample-buttons {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }

  .sample-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 18px;
    border: 2px solid #000;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    background: white;
    color: #000;
    min-width: 140px;
    flex: 1;
    max-width: 200px;
  }

  .sample-btn:hover {
    background: #000;
    color: white;
  }

  .sample-btn:active {
    transform: translateY(1px);
  }

  .form {
    margin-bottom: 30px;
  }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  .form-group label {
    margin-bottom: 5px;
    font-weight: 600;
    color: #000;
  }

  .form-group input,
  .form-group select {
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.2s;
    background: white;
    color: #000;
  }

  .form-group input:focus,
  .form-group select:focus {
    outline: none;
    border-color: #000;
  }

  .predict-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    width: 100%;
    padding: 16px;
    background: #000;
    color: white;
    border: 2px solid #000;
    border-radius: 6px;
    font-size: 1.2rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .predict-btn:hover:not(:disabled) {
    background: white;
    color: #000;
  }

  .predict-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .error {
    background: #f9f9f9;
    border: 2px solid #ddd;
    border-radius: 6px;
    padding: 24px;
    margin: 20px 0;
  }

  .error-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }

  .error-header h3 {
    margin: 0;
    color: #000;
    font-size: 1.25rem;
  }

  .error p {
    margin: 8px 0;
    color: #333;
    line-height: 1.5;
  }

  .error small {
    color: #666;
  }

  .result {
    background: #f9f9f9;
    border: 2px solid #ddd;
    border-radius: 6px;
    padding: 24px;
    margin: 20px 0;
  }

  .result-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    justify-content: center;
  }

  .result-header h3 {
    margin: 0;
    color: #000;
    font-size: 1.25rem;
  }

  .age-result {
    text-align: center;
    margin: 24px 0;
    padding: 24px;
    background: white;
    border-radius: 6px;
    border: 1px solid #ddd;
  }

  .age-display {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
  }

  .age-icon {
    opacity: 0.8;
  }

  .age-info {
    text-align: left;
  }

  .age-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: #000;
    margin: 0;
    line-height: 1;
  }

  .age-label {
    font-size: 1.1rem;
    color: #666;
    margin: 4px 0 0 0;
  }

  .details {
    margin: 20px 0;
    padding: 20px;
    background: white;
    border-radius: 6px;
    border: 1px solid #ddd;
  }

  .detail-item {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 12px 0;
    color: #333;
  }

  .detail-item svg {
    color: #000;
    flex-shrink: 0;
  }

  .detail-item span {
    line-height: 1.4;
  }

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  .spinning {
    animation: spin 1s linear infinite;
  }

  @media (max-width: 768px) {
    .container {
      margin: 10px;
      padding: 20px;
    }

    header h1 {
      font-size: 2rem;
    }

    header p {
      font-size: 1rem;
    }

    .form-grid {
      grid-template-columns: 1fr;
      gap: 15px;
    }

    .sample-buttons {
      flex-direction: column;
      gap: 12px;
      align-items: center;
    }

    .sample-btn {
      justify-content: center;
      padding: 14px 20px;
      min-width: 200px;
      max-width: 250px;
    }

    .student-info {
      margin-top: 10px;
      padding: 8px 16px;
    }

    .student-info p {
      font-size: 0.9rem;
    }

    .age-display {
      flex-direction: column;
      gap: 12px;
    }

    .age-info {
      text-align: center;
    }

    .age-number {
      font-size: 2.2rem;
    }

    .predict-btn {
      font-size: 1.1rem;
      padding: 14px;
    }

    .detail-item {
      flex-wrap: wrap;
      gap: 8px;
    }
  }
</style>
