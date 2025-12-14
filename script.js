async function predict() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    if (!title || !content) {
        alert("Please enter both title and content");
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            content: content
        })
    });

    const data = await response.json();

    document.getElementById("label").innerText = data.category;
    document.getElementById("confidence").innerText =
        (data.confidence * 100).toFixed(2) + "%";
}
