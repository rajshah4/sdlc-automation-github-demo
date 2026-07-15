const pets = [
  { id: "pet-100", name: "Mochi", species: "cat", size: "small", status: "available", tags: ["calm", "indoor"], fee: "$75" },
  { id: "pet-101", name: "Scout", species: "dog", size: "medium", status: "available", tags: ["active", "family"], fee: "$125" },
  { id: "pet-102", name: "Pip", species: "rabbit", size: "small", status: "available", tags: ["quiet", "indoor"], fee: "$45" },
  { id: "pet-103", name: "Nova", species: "dog", size: "medium", status: "pending", tags: ["active", "training"], fee: "$110" },
];

function renderResults() {
  const query = document.querySelector("#query").value.trim().toLowerCase();
  const species = document.querySelector("#species").value;
  const size = document.querySelector("#size").value;
  const list = document.querySelector("#results");
  list.innerHTML = "";

  const matches = pets.filter((pet) => {
    return pet.name.toLowerCase().includes(query)
      && (species === "" || pet.species === species)
      && (size === "" || pet.size === size)
      && pet.status === "available";
  });

  if (matches.length === 0) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = "No available pets match this search.";
    list.appendChild(empty);
    return;
  }

  for (const pet of matches) {
    const item = document.createElement("li");
    item.className = "pet";
    item.innerHTML = `<strong>${pet.name}</strong><span>${pet.species} · ${pet.size} · ${pet.tags.join(", ")}</span><b>${pet.fee}</b>`;
    list.appendChild(item);
  }
}

document.querySelector("#search-button").addEventListener("click", renderResults);
renderResults();
