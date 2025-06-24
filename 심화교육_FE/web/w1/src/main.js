const menuData = [
  { id: 1, name: "떡볶이", price: 3000, image: "https://via.placeholder.com/300x200?text=떡볶이" },
  { id: 2, name: "순대", price: 3500, image: "https://via.placeholder.com/300x200?text=순대" },
  { id: 3, name: "튀김", price: 2500, image: "https://via.placeholder.com/300x200?text=튀김" },
  { id: 4, name: "김밥", price: 2000, image: "https://via.placeholder.com/300x200?text=김밥" },
  { id: 5, name: "라면", price: 4000, image: "https://via.placeholder.com/300x200?text=라면" },
  { id: 6, name: "쫄면", price: 4000, image: "https://via.placeholder.com/300x200?text=쫄면" }
];

const state = {}; // { id: 수량 }
const menuContainer = document.getElementById("menu-container");
const totalPriceEl = document.getElementById("total-price");

function renderMenus() {
  menuContainer.innerHTML = "";
  menuData.forEach(item => {
    const quantity = state[item.id] || 0;
    const card = document.createElement("div");
    card.className = "menu-card";
    card.innerHTML = `
      <img src="${item.image}" alt="${item.name}">
      <h3>${item.name}</h3>
      <p>₩${item.price.toLocaleString()}</p>
      <div class="controls">
        <button onclick="changeQuantity(${item.id}, -1)">−</button>
        <span>${quantity}</span>
        <button onclick="changeQuantity(${item.id}, 1)">+</button>
      </div>
    `;
    menuContainer.appendChild(card);
  });
}

window.changeQuantity = function (id, delta) {
  state[id] = (state[id] || 0) + delta;
  if (state[id] < 0) state[id] = 0;
  updateTotal();
  renderMenus();
};

function updateTotal() {
  let total = 0;
  for (const item of menuData) {
    const qty = state[item.id] || 0;
    total += item.price * qty;
  }
  totalPriceEl.textContent = `₩${total.toLocaleString()}`;
}

// 초기 렌더링
renderMenus();
updateTotal();