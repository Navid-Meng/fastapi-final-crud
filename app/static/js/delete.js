async function deleteProduct(productId){
    try{
        const response = await fetch(`/api/products/${productId}`, {
            method: 'DELETE',
            header: {
                'Content-Type': 'application/json'
            }
        })
        .then (response => {
            if (!response.ok){
                throw new Error('Network response was not ok')
            }
            window.location.href = '/products/read'
        })   
        .catch (error => {
            console.error('Error deleting product: ', error)
        })
    } catch(error){
        console.error("Error deleting product: ", error)
    }
}