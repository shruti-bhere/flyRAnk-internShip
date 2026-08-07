document.addEventListener("DOMContentLoaded", () => {
    initChatInterface();
});

function initChatInterface() {
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const chatOutput = document.getElementById("chatOutput");
    const suggestionButtons = document.querySelectorAll(".suggest-btn");
    
    // Generate an isolated, transient configuration identifier for the single session conversation tracking
    const targetSessionId = "session_" + Math.random().toString(36).substring(2, 11);

    // Setup input trigger routing for quick-action template questions
    suggestionButtons.forEach(button => {
        button.addEventListener("click", () => {
            const cleaningPrompt = button.textContent.replace(/^"|"$/g, '');
            chatInput.value = cleaningPrompt;
            chatForm.dispatchEvent(new Event("submit"));
        });
    });

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const rawPrompt = chatInput.value.trim();
        if (!rawPrompt) return;

        // Clear input area immediately
        chatInput.value = "";

        // Render User block inside workspace
        appendMessage("user", rawPrompt);

        // Render Bot block template to buffer incoming data streams
        const botMessageWrapper = appendMessage("bot", "🧬 Connecting to inference matrix...");
        
        try {
            const response = await fetch("http://localhost:8000/api/v1/chat/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: rawPrompt, conversation_id: targetSessionId })
            });

            if (!response.ok) throw new Error("Inference pipeline broken.");

            // Clear text placeholder before parsing active streams
            botMessageWrapper.innerHTML = "";
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let incompleteChunk = "";

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const decodedString = decoder.decode(value, { stream: true });
                const combinedLines = (incompleteChunk + decodedString).split("\n\n");
                
                // Store incomplete tail records securely
                incompleteChunk = combinedLines.pop();

                for (const explicitLine of combinedLines) {
                    if (explicitLine.startsWith("data: ")) {
                        try {
                            const coreData = JSON.parse(explicitLine.substring(6));
                            if (coreData.text) {
                                // Append raw word chunks straight to active UI view node
                                botMessageWrapper.innerHTML += coreData.text;
                                chatOutput.scrollTop = chatOutput.scrollHeight;
                            }
                        } catch (parseError) {
                            console.debug("Transient line parse execution bypassed.");
                        }
                    }
                }
            }
        } catch (error) {
            console.error("AI pipeline communication error details:", error);
            botMessageWrapper.innerHTML = `<span style="color: #ef4444;">⚠️ Core connection interrupted. Ensure local Ollama instance is actively running.</span>`;
        }
    });

    function appendMessage(sender, textualContent) {
        const messageBox = document.createElement("div");
        messageBox.className = `chat-message ${sender}`;
        messageBox.innerHTML = textualContent;
        chatOutput.appendChild(messageBox);
        chatOutput.scrollTop = chatOutput.scrollHeight;
        return messageBox;
    }
}