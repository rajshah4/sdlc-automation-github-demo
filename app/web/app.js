const pets = [
  { id: "pet-100", name: "Mochi", species: "cat", status: "available", tags: ["calm", "indoor"], fee: "$75", ageMonths: 18 },
  { id: "pet-101", name: "Scout", species: "dog", status: "available", tags: ["active", "family"], fee: "$125", ageMonths: 28 },
  { id: "pet-102", name: "Pip", species: "rabbit", status: "available", tags: ["quiet", "indoor"], fee: "$45", ageMonths: 9 },
  { id: "pet-103", name: "Nova", species: "dog", status: "pending", tags: ["active", "training"], fee: "$110", ageMonths: 14 },
];

function feeToCents(feeStr) {
  return Math.round(parseFloat(feeStr.replace("$", "")) * 100);
}

function getAgeRange(category) {
  switch (category) {
    case "puppy":
      return { min: 0, max: 12 };
    case "adult":
      return { min: 13, max: 84 };
    case "senior":
      return { min: 85, max: null };
    default:
      return { min: null, max: null };
  }
}

function renderResults() {
  const query = document.querySelector("#query").value.trim().toLowerCase();
  const species = document.querySelector("#species").value;
  const familyFriendlyOnly = document.querySelector("#family-friendly").checked;
  const maxFeeInput = document.querySelector("#max-fee").value;
  const maxFeeCents = maxFeeInput !== "" ? Math.round(parseFloat(maxFeeInput) * 100) : null;
  const ageCategory = document.querySelector("#age-category").value;
  const ageRange = getAgeRange(ageCategory);
  const list = document.querySelector("#results");
  list.innerHTML = "";

  const matches = pets.filter((pet) => {
    const ageMatches =
      (ageRange.min === null || pet.ageMonths >= ageRange.min) &&
      (ageRange.max === null || pet.ageMonths <= ageRange.max);
    return pet.name.toLowerCase().includes(query)
      && (species === "" || pet.species === species)
      && (!familyFriendlyOnly || pet.tags.includes("family"))
      && pet.status === "available"
      && (maxFeeCents === null || feeToCents(pet.fee) <= maxFeeCents)
      && ageMatches;
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
document.querySelector("#family-friendly").addEventListener("change", renderResults);
document.querySelector("#max-fee").addEventListener("input", renderResults);
document.querySelector("#age-category").addEventListener("change", renderResults);
renderResults();
