const pets = [
  { id: "pet-100", name: "Mochi", species: "cat", status: "available", tags: ["calm", "indoor"], fee: "$75", ageMonths: 18 },
  { id: "pet-101", name: "Scout", species: "dog", status: "available", tags: ["active", "family"], fee: "$125", ageMonths: 28 },
  { id: "pet-102", name: "Pip", species: "rabbit", status: "available", tags: ["quiet", "indoor"], fee: "$45", ageMonths: 9 },
  { id: "pet-103", name: "Nova", species: "dog", status: "pending", tags: ["active", "training"], fee: "$110", ageMonths: 14 },
];

function formatAge(months) {
  if (months < 0) {
    throw new Error("Age cannot be negative");
  }
  
  const years = Math.floor(months / 12);
  const remainingMonths = months % 12;
  
  const parts = [];
  if (years > 0) {
    parts.push(years === 1 ? "1 year" : `${years} years`);
  }
  if (remainingMonths > 0) {
    parts.push(remainingMonths === 1 ? "1 month" : `${remainingMonths} months`);
  }
  
  if (parts.length === 0) {
    return "0 months";
  }
  
  return parts.join(" ");
}

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
    const formattedAge = formatAge(pet.ageMonths);
    item.innerHTML = `<strong>${pet.name}</strong><span>${pet.species} · ${formattedAge} · ${pet.tags.join(", ")}</span><b>${pet.fee}</b><span class="sr-only">Age in months: ${pet.ageMonths}</span>`;
    list.appendChild(item);
  }
}

document.querySelector("#search-button").addEventListener("click", renderResults);
renderResults();
