
function deleteProduct(productId){
    fetch(`/api/products/${productId}`, {
        method: 'DELETE',
        header: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        window.location.href = '/products/read'
    })
    .catch(error => {
        console.error('Error deleting product:', error);
        // Optionally display an error message or handle the error
    });
}

document.addEventListener('click', function(event){
    if (event.target.classList.contains('delete-product')){
        const productId = event.target.getAttribute('data-product-id');
        if(confirm(`Are you sure you want to delete product ${productId}?`)){
            deleteProduct(productId);
        }
    }
});