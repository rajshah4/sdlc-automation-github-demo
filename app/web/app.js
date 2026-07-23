const pets = [
  { id: "pet-100", name: "Mochi", species: "cat", status: "available", tags: ["calm", "indoor"], fee: "$75" },
  { id: "pet-101", name: "Scout", species: "dog", status: "available", tags: ["active", "family"], fee: "$125" },
  { id: "pet-102", name: "Pip", species: "rabbit", status: "available", tags: ["quiet", "indoor"], fee: "$45" },
  { id: "pet-103", name: "Nova", species: "dog", status: "pending", tags: ["active", "training"], fee: "$110" },
];

function renderResults() {
  const query = document.querySelector("#query").value.trim().toLowerCase();
  const species = document.querySelector("#species").value;
  const list = document.querySelector("#results");
  list.innerHTML = "";

  // KAN-125: Default customer-facing search must show ONLY available pets.
  // Pending pets should never appear unless explicitly requested by support staff.
  const matches = pets.filter((pet) => {
    const matchesQuery = pet.name.toLowerCase().includes(query);
    const matchesSpecies = species === "" || pet.species === species;
    const isAvailable = pet.status === "available";
    
    return matchesQuery && matchesSpecies && isAvailable;
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
    item.innerHTML = `<strong>${pet.name}</strong><span>${pet.species} · ${pet.tags.join(", ")}</span><b>${pet.fee}</b>`;
    list.appendChild(item);
  }
}

document.querySelector("#search-button").addEventListener("click", renderResults);
renderResults();
