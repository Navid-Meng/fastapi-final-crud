document.getElementById('updateProductForm').addEventListener('submit', async function(event){
    event.preventDefault();

    let productId = document.getElementById('productId').value;
    let productName = document.getElementById('productName').value;
    let price = document.getElementById('price').value;
    let stockQty = document.getElementById('stockQty').value;
    let categoryId = document.getElementById('categoryId').value;

    let formData = {
        productName: productName,
        price: parseFloat(price),
        stockQty: parseInt(stockQty),
        categoryId: parseInt(categoryId)
    }

    try {
        let response = await fetch(`/api/products/${parseInt(productId)}`, {
            method: 'PUT',
            method: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })

        if (response.ok){
            window.location.href = '/products/read'
        } else {
            const responseMessage = document.getElementById('responseMessage');
            responseMessage.innerText = `Product name "${productName}" already exists`;
            responseMessage.classList.add('alert', 'alert-danger');
        }

    } catch(error){
        console.error(error);
    }
})