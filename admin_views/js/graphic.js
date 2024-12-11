function fetchSalesData() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/sales_data', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const salesData = JSON.parse(xhr.responseText);
            renderSalesChart(salesData);
        } else {
            console.error("Erro ao buscar os dados de vendas:", xhr.statusText);
        }
    };
    xhr.onerror = function () {
        console.error("Erro de rede ao tentar buscar os dados.");
    };
    xhr.send();
}

function renderSalesChart(salesData) {
    const labels = salesData.map(item => item.sale_date);
    const dataSales = salesData.map(item => item.total_sales);
    
    const ctx = document.getElementById('salesChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Vendas Totais',
                data: dataSales,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Chama a função para buscar os dados quando a página é carregada
window.onload = fetchSalesData;
