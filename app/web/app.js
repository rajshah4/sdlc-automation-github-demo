const pets = [
  { id: "pet-100", name: "Mochi", species: "cat", status: "available", tags: ["calm", "indoor"], feeCents: 7500 },
  { id: "pet-101", name: "Scout", species: "dog", status: "available", tags: ["active", "family"], feeCents: 12500 },
  { id: "pet-102", name: "Pip", species: "rabbit", status: "available", tags: ["quiet", "indoor"], feeCents: 4500 },
  { id: "pet-103", name: "Nova", species: "dog", status: "pending", tags: ["active", "training"], feeCents: 11000 },
];

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function formatFee(feeCents) {
  return currency.format(feeCents / 100);
}

function parseMaxFeeCents() {
  const rawValue = document.querySelector("#max-fee").value.trim();
  if (rawValue === "") {
    return { maxFeeCents: null, error: "" };
  }

  const feeDollars = Number(rawValue);
  if (!Number.isFinite(feeDollars) || feeDollars < 0) {
    return { maxFeeCents: null, error: "Enter a maximum fee of 0 or more." };
  }

  return { maxFeeCents: Math.round(feeDollars * 100), error: "" };
}

function renderResults() {
  const query = document.querySelector("#query").value.trim().toLowerCase();
  const species = document.querySelector("#species").value;
  const { maxFeeCents, error } = parseMaxFeeCents();
  const list = document.querySelector("#results");
  const summary = document.querySelector("#result-summary");
  const feeError = document.querySelector("#fee-error");
  list.innerHTML = "";
  feeError.textContent = error;

  if (error) {
    summary.textContent = "Adjust the adoption fee filter to continue.";
    return;
  }

  const matches = pets.filter((pet) => {
    return pet.name.toLowerCase().includes(query)
      && (species === "" || pet.species === species)
      && (maxFeeCents === null || pet.feeCents <= maxFeeCents)
      && pet.status === "available";
  });

  summary.textContent = `${matches.length} available pet${matches.length === 1 ? "" : "s"} match this search.`;

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
    item.innerHTML = `<strong>${pet.name}</strong><span>${pet.species} · ${pet.tags.join(", ")}</span><b>${formatFee(pet.feeCents)}</b>`;
    list.appendChild(item);
  }
}

document.querySelector("#search-button").addEventListener("click", renderResults);
renderResults();
