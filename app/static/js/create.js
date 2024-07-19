document.getElementById('createProductForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    let productName = document.getElementById('productName').value;
    let price = document.getElementById('price').value;
    let stockQty = document.getElementById('stockQty').value;
    let categoryId = document.getElementById('categoryId').value;

    let formData = {
        productName: productName,
        price: parseFloat(price),
        stockQty: parseInt(stockQty),
        categoryId: parseInt(categoryId),
        is_active: true
    };
    
    try {
        let response = await fetch('/api/products/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            // Redirect to /products/read after successful creation
            window.location.href = '/products/read';
        } else {
            const responseMessage = document.getElementById('responseMessage');
            responseMessage.innerText = `Product name "${productName}" already exists`;
            responseMessage.classList.add('alert', 'alert-danger');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});