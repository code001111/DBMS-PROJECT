// Update cart count on page load
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
});

// Update cart count
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;
}

// When cart is modified, update the count
const originalSetItem = localStorage.setItem;
localStorage.setItem = function(key, value) {
    originalSetItem.apply(this, arguments);
    if (key === 'cart') {
        updateCartCount();
    }
};
