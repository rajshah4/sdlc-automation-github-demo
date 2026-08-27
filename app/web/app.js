const pets = [
  { id: "pet-100", name: "Mochi", species: "cat", status: "available", tags: ["calm", "indoor"], fee: "$75", baseFee: "$50", vaccinationFee: "$15", microchipFee: "$10" },
  { id: "pet-101", name: "Scout", species: "dog", status: "available", tags: ["active", "family"], fee: "$125", baseFee: "$90", vaccinationFee: "$20", microchipFee: "$15" },
  { id: "pet-102", name: "Pip", species: "rabbit", status: "available", tags: ["quiet", "indoor"], fee: "$45", baseFee: "$30", vaccinationFee: "$10", microchipFee: "$5" },
  { id: "pet-103", name: "Nova", species: "dog", status: "pending", tags: ["active", "training"], fee: "$110", baseFee: "$80", vaccinationFee: "$20", microchipFee: "$10" },
];

function renderResults() {
  const query = document.querySelector("#query").value.trim().toLowerCase();
  const species = document.querySelector("#species").value;
  const list = document.querySelector("#results");
  list.innerHTML = "";

  const matches = pets.filter((pet) => {
    return pet.name.toLowerCase().includes(query)
      && (species === "" || pet.species === species)
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
    item.innerHTML = `
      <strong>${pet.name}</strong>
      <span>${pet.species} · ${pet.tags.join(", ")}</span>
      <div class="fee-breakdown">
        <div class="fee-item">Base Fee: ${pet.baseFee}</div>
        <div class="fee-item">Vaccination: ${pet.vaccinationFee}</div>
        <div class="fee-item">Microchip: ${pet.microchipFee}</div>
        <div class="fee-total">Total: <b>${pet.fee}</b></div>
      </div>
    `;
    list.appendChild(item);
  }
}

document.querySelector("#search-button").addEventListener("click", renderResults);
renderResults();
