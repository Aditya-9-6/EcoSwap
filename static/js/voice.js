document.addEventListener('DOMContentLoaded', () => {
    const micBtn = document.getElementById('micBtn');
    const searchInput = document.getElementById('searchInput');
    const searchForm = document.getElementById('searchForm');
    const voiceStatus = document.getElementById('voiceStatus');

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.continuous = false;
        recognition.lang = 'en-US';

        micBtn.addEventListener('click', () => {
            recognition.start();
            voiceStatus.classList.remove('hidden');
            micBtn.classList.add('text-green-600');
            voiceStatus.textContent = 'Listening...';
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            searchInput.value = transcript;
            voiceStatus.textContent = `Heard: "${transcript}"... Searching...`;
            micBtn.classList.remove('text-green-600');
            setTimeout(() => {
                searchForm.submit();
            }, 800);
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            voiceStatus.textContent = 'Error listening. Try again.';
            micBtn.classList.remove('text-green-600');
            setTimeout(() => {
                voiceStatus.classList.add('hidden');
            }, 3000);
        };

        recognition.onend = () => {
            // voiceStatus.classList.add('hidden'); // Keep visible for "Searching..." status
        };
    } else {
        if (micBtn) {
            micBtn.style.display = 'none';
        }
        console.warn('Web Speech API not supported in this browser.');
    }
});
