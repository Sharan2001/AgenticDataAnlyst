// // Upload DB
// async function uploadDB() {
//   const file = document.getElementById("dbFile").files[0];

//   if (!file) return alert("Select file");

//   const formData = new FormData();
//   formData.append("file", file);

//   const res = await fetch("/upload", {
//     method: "POST",
//     body: formData
//   });

//   const data = await res.json();
//   alert(data.message);

//   loadDBs();
// }

// // Load DBs
// async function loadDBs() {
//   const res = await fetch("/list-dbs");
//   const files = await res.json();

//   const dropdown = document.getElementById("dbDropdown");
//   dropdown.innerHTML = "";

//   files.forEach(f => {
//     const opt = document.createElement("option");
//     opt.value = f;
//     opt.textContent = f;
//     dropdown.appendChild(opt);
//   });
// }

// // Submit query
// async function submitQuery() {
//   const db = document.getElementById("dbDropdown").value;
//   const question = document.getElementById("question").value;

//   if (!db || !question) return alert("Fill everything");

//   const res = await fetch(
//     `/analyze?question=${encodeURIComponent(question)}&db_name=${db}`
//   );

//   const data = await res.json();

//   document.getElementById("result").innerText =
//     JSON.stringify(data, null, 2);
// }

// window.onload = loadDBs;

// frontend/home.js

window.onload = async function () {
    await loadDBs();
};

// ------------------------
// Load DBs into dropdown
// ------------------------
async function loadDBs() {
    const res = await fetch("/list-dbs");
    const files = await res.json();
    const dropdown = document.getElementById("dbDropdown");
    dropdown.innerHTML = "";
    files.forEach(f => {
        const opt = document.createElement("option");
        opt.value = f;
        opt.textContent = f;
        dropdown.appendChild(opt);
    });
}

// ------------------------
// Upload DB file
// ------------------------
async function uploadDB() {
    const fileInput = document.getElementById("dbFile");
    const file = fileInput.files[0];
    if (!file) {
        alert("Select a file to upload!");
        return;
    }

    const submitBtn = document.querySelector("button.upload-btn");
    submitBtn.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData,
        });
        if (!res.ok) throw new Error("Upload failed");

        alert("DB uploaded successfully!");
        fileInput.value = "";
        await loadDBs(); // refresh dropdown
    } catch (err) {
        alert("Error uploading DB: " + err.message);
    } finally {
        submitBtn.disabled = false;
    }
}

// ------------------------
// Add message to chat
// ------------------------
function addMessage(content, sender) {
    const chatWindow = document.getElementById("chat-window");
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;

    // Render table if content has result
    if (typeof content === "object" && content.result) {
        content.result.forEach(res => {
            const table = document.createElement("table");
            table.className = "result-table";

            const thead = document.createElement("thead");
            const headerRow = document.createElement("tr");
            res.columns.forEach(col => {
                const th = document.createElement("th");
                th.textContent = col;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            const tbody = document.createElement("tbody");
            res.rows.forEach(row => {
                const tr = document.createElement("tr");
                row.forEach(cell => {
                    const td = document.createElement("td");
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
            table.appendChild(tbody);
            msg.appendChild(table);
        });
    } else {
        msg.textContent = content;
    }

    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ------------------------
// Submit question to backend
// ------------------------
async function submitQuery() {
    const db = document.getElementById("dbDropdown").value;
    const question = document.getElementById("question").value.trim();
    const submitBtn = document.getElementById("submit");
    const uploadBtn = document.getElementById("upload-btn");
    

    if (!db || !question) {
        alert("Select a DB and type a question!");
        return;
    }

    document.getElementById("question").value = "";
    addMessage(question, "user");

    // Disable submit button
    submitBtn.disabled = true;
    uploadBtn.disabled = true;

    // Animated typing bubble
    const chatWindow = document.getElementById("chat-window");
    const placeholder = document.createElement("div");
    placeholder.className = "message agent typing";
    placeholder.innerHTML = `<span></span><span></span><span></span>`;
    chatWindow.appendChild(placeholder);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const res = await fetch(
            `/analyze?question=${encodeURIComponent(question)}&db_name=${encodeURIComponent(db)}`
        );
        if (!res.ok) throw new Error("Server error");

        const latestQA = await res.json();

        // Remove typing bubble
        placeholder.remove();

        // Append actual response
        latestQA.forEach(item => {
            if (item.role === "agent") {
                addMessage(item.content, "agent");
            }
        });
    } catch (err) {
        placeholder.textContent = "❌ Error: " + err.message;
    } finally {
        submitBtn.disabled = false;
    }
}


// function addMessage(text, sender) {
//     const chatWindow = document.getElementById("chat-window");
//     const msg = document.createElement("div");
//     msg.className = `message ${sender}`;
//     msg.textContent = text;
//     chatWindow.appendChild(msg);
//     chatWindow.scrollTop = chatWindow.scrollHeight; // auto-scroll
// }

// Submit question to backend and append latest Q/A
// async function submitQuery() {
//     const db = document.getElementById("dbDropdown").value;
//     const question = document.getElementById("question").value.trim();

//     if (!db || !question) {
//         alert("Select a DB and type a question!");
//         return;
//     }

//     document.getElementById("question").value = ""; // clear input
//     addMessage(question, "user"); // show user's question immediately

//     try {
//         const res = await fetch(
//             `/analyze?question=${encodeURIComponent(question)}&db_name=${encodeURIComponent(db)}`
//         );
//         if (!res.ok) throw new Error("Server error");

//         const latestQA = await res.json(); // [{role:"user", content}, {role:"agent", content}]
//         latestQA.forEach(item => {
//             if (item.role === "agent") {
//                 addMessage(item.content, "agent"); // show agent response
//             }
//         });
//     } catch (err) {
//         addMessage("Error: " + err.message, "agent");
//     }
// }