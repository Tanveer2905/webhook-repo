async function fetchEvents() {
    const res = await fetch("/events");
    const data = await res.json();

    const feed = document.getElementById("feed");
    feed.innerHTML = "";

    data.forEach(text => {
        const li = document.createElement("li");
        li.classList.add("event");

        let type = "push";
        if (text.includes("pull request")) type = "pr";
        if (text.includes("merged branch")) type = "merge";

        li.classList.add(type);

        const badge = document.createElement("span");
        badge.classList.add("badge", type);
        badge.textContent = type.toUpperCase();

        const content = document.createElement("div");
        content.textContent = text;

        li.appendChild(content);
        li.appendChild(badge);

        feed.appendChild(li);
    });
}

setInterval(fetchEvents, 15000);
fetchEvents();
