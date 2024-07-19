function fetchProducts(){
    fetch('/api/products')
        .then(response => {
            if (!response.ok){
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(page => {
            console.log("Page:", page);
            const productTable = document.getElementById('product-table').getElementsByTagName('tbody')[0];
            productTable.innerHTML = '';
            page.items.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                <td>${product.id}</td>
                <td>${product.productName}</td>
                <td>${product.price}</td>
                <td>${product.stockQty}</td>
                <td>
                    <a href="/products/update/${product.id}" class="btn btn-success">Edit</a>
                    <a href="#" class="btn btn-danger delete-product" data-product-id="${ product.id }">Delete</a>
                </td>
                `;
                productTable.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching data: ', error);
        });
}
document.addEventListener('DOMContentLoaded', fetchProducts);

productTable.addEventListener('click', async function(event){
    if (event.target.classList.contains('delete-product')){
        try{
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
        } catch(error){
            console.error("Error delting product: ", error);
        }
    }
})