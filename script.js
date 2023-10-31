const items = []
const latestOrderInfo = document.getElementById('latest-order-info');
document.addEventListener('DOMContentLoaded', () => {
  const menu = document.querySelector('#menu');
  const orderForm = document.querySelector('#order-form');
  const orderSummary = document.querySelector('#order-summary');
  const loader = document.querySelector('#loader');
  const confirmation = document.querySelector('#confirmation');
  const menuContainer = document.querySelector('#menu');

  let total = 0;

  // Helper function to format currency
  function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
  }

  // Helper function to update the order summary
  function updateOrderSummary() {
    total = 0;

    // Clear the current order summary
    orderSummary.innerHTML = '';

    const summaryHeader = document.createElement('h3')
    summaryHeader.textContent = 'Order Summary:'
    orderSummary.appendChild(summaryHeader)
    const emptyOrder = document.createElement('p')
    emptyOrder.id = 'empty-order';
    emptyOrder.textContent = 'Empty Order'

    // Calculate the total price of the items ordered
    items.forEach(item => {
      const price = item.price;
      const quantity = item.quantity;
      const subtotal = quantity * price;
      total += subtotal;

      // Create a list item element for each item ordered
      const p = document.createElement('p');
      p.textContent = `${item.name} (${quantity} x ${formatCurrency(price)} = ${formatCurrency(subtotal)})`;
      if (subtotal > 0) {
        orderSummary.appendChild(p);
      }
    });
    if (total <= 0) {
      orderSummary.appendChild(emptyOrder);
    }

    // Add the total price to the order summary
    const res = document.createElement('p');
    res.classList.add('total');
    res.textContent = `Total: ${formatCurrency(total)}`;
    orderSummary.appendChild(res);
  }

  // Load the menu from the server
  async function loadMenu() {
    try {
      const response = await fetch('http://localhost:8000/menu');
      const data = await response.json();
      console.table(data.items);
      for (key in data.items) {
        data.items[key]['quantity'] = 0;
        items.push(data.items[key])
      }
      renderMenu(items);
    } catch (error) {
      console.log(error);
      alert('There was an error loading the menu. Please try again later.');
    }
  }


  function renderMenu(items) {
    items.forEach((item, index) => {
      const card = document.createElement('div');
      card.className = 'card';

      const title = document.createElement('h3');
      title.textContent = item.name + " ($" + item.price + ")";
      card.appendChild(title);

      const description = document.createElement('p');
      description.textContent = item.description;
      card.appendChild(description);

      const quantityLabel = document.createElement('label');
      quantityLabel.textContent = 'Quantity:';
      const quantityInput = document.createElement('input');
      quantityInput.type = 'number';
      quantityInput.min = 0;
      quantityInput.max = 5;
      quantityInput.value = 0;
      quantityInput.id = item.id;
      quantityLabel.appendChild(quantityInput);
      card.appendChild(quantityLabel);

      menuContainer.appendChild(card);
    });
  }


  // Submit the order to the server
  async function submitOrder(event) {
    event.preventDefault();

    const order = { 'items': items };
    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(order)
    };
    const response = await fetch('http://localhost:8000/orders', options);

    // Show a confirmation message if the order was successful
    if (response.ok) {
      alert('Order Was Successful!')
      updateOrderSummary();
    } else {
      const details = await response.json()
      alert('There was an error submitting your order. Please try again later.' + `\n${details['message']}`);
    }
  }



  // Event listeners
  orderForm.addEventListener('submit', submitOrder);

  menu.addEventListener('change', event => {
    updateItemQuantity(Number(event.target.id), Number(event.target.value));
    updateOrderSummary();
  });

  // Load the menu when the page loads
  loadMenu().then(() => {
    loader.style.display = "none";
  });
});



function updateItemQuantity(id, value) {
  const itemIndex = items.findIndex(item => item.id === id);
  if (itemIndex === -1) {
    throw new Error('ID mismatch!');
  }
  items[itemIndex]['quantity'] = value;
}

function displayLatestOrder() {
  getLastOrderAsPromise()
    .then(items => {
      let res = '<p>'
      items.forEach(item => res += `${item.name}: ${item.quantity}<br>`);
      console.log("Latest order items:", items);
      res += '</p>'
      latestOrderInfo.innerHTML = res;
    })
    .catch(error => {
      console.error("Error while getting latest order:", error);
      alert('No recent order found')
    });
}

function getLastOrderAsPromise() {
  return new Promise(async (resolve, reject) => {
    try {
      const options = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      };
      const response = await fetch('http://localhost:8000/latest-order', options);
      const data = await response.json();
      resolve(data['items']);
    } catch (error) {
      reject(error);
    }
  });
}


//This is here as an example
async function printHelloWorld() {
  const options = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  };
  const response = await fetch('http://localhost:8000/hello', options);
  return response;
}

async function getHello() {
  const unparsedResponse = await printHelloWorld();
  const parsedResponse = await unparsedResponse.json()
  return parsedResponse;
}

const finalRes = getHello();
finalRes.then((res)=> console.log(res));
/*
List of endpoints:
  GET - http://localhost:8000/hello -> {'Hello': 'World'} Here as an example
  GET - http://localhost:8000/menu -> {'items': menu} A dict of the menu
  POST - http://localhost:8000/latest-order -> A dict of the latest order
  POST - http://localhost:8000/orders ->
  An endpoint to handle an order. The order is in the http body in this format const order = { 'items': items }; (needs to be json stringified)

*/
