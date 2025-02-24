const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatForm = document.getElementById('chat-form');

// 获取 CSRF 令牌
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // 显示用户消息
    chatBox.innerHTML += `<p><strong>👤 你:</strong> ${message}</p>`;
    userInput.value = '';

    // 发送 POST 请求到后端
    try {
        const response = await fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken  // 添加 CSRF 令牌
            },
            body: new URLSearchParams({ message: message })
        });

        // 实时显示流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        chatBox.innerHTML += '<p><strong>🤖 AI:</strong> ';
        let aiResponse = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            aiResponse += chunk;
            chatBox.innerHTML += chunk;
            chatBox.scrollTop = chatBox.scrollHeight; // 自动滚动到底部
        }

        chatBox.innerHTML += '</p>';
    } catch (error) {
        console.error('Error:', error);
        chatBox.innerHTML += '<p><strong>错误:</strong> 无法连接到 AI 服务</p>';
    }
});