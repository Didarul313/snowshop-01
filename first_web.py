import http.server
import socketserver
import json
# Import your chatbot functionality
from chatbot import get_chatbot_response  # Assuming chatbot.py has this function

# Load product data from JSON file
def load_products():
    with open('products.json', 'r') as file:
        return json.load(file)

products = load_products()  # Load products from JSON file

# Shopping cart to hold selected products
cart = []

# Function to handle product addition to cart
def add_to_cart(product_id):
    global cart
    for product in products:
        if product["id"] == product_id:
            cart.append(product)
            return True
    return False

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/chat":
            content_length = int(self.headers['Content-Length'])  # Get the length of the message
            post_data = self.rfile.read(content_length).decode('utf-8')  # Read the message data

            # Here, you'll call your chatbot function to get a response
            user_message = json.loads(post_data)["message"]  # Assuming JSON format like { "message": "Hi" }
            bot_response = get_chatbot_response(user_message)  # Call the chatbot function

            # Respond with the chatbot's message
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"response": bot_response})
            self.wfile.write(response.encode())
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>My Dynamic Product Selling Web</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
                <style>
                    /* Styles for the page */
                    body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 0; color: #333; }
                    nav { display: flex; justify-content: space-between; align-items: center; background-color: #333; padding: 10px; }
                    nav a { color: #888; text-decoration: none; padding: 5px 10px; font-size: 1rem; }
                    nav a:hover { color: #ff5e62; }
                    header { background: linear-gradient(45deg, #ff5e62, #ff9966); color: white; text-align: center; padding: 10px; }
                    header h1 { font-size: 2.5rem; margin: 0; }
                    .product-section { display: flex; justify-content: space-around; flex-wrap: wrap; padding: 20px; background-color: white; }
                    .product-card { background-color: #fff; padding: 10px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); text-align: center; width: 220px; margin: 10px; transition: transform 0.3s; }
                    .product-card:hover { transform: scale(1.05); }
                    .product-card img { width: 100%; border-radius: 10px; }
                    .product-card h2 { font-size: 1.3rem; margin: 10px 0; }
                    .product-card p { color: #666; font-size: 1rem; margin: 5px 0; }
                    .product-card button { background-color: #ff5e62; color: white; border: none; padding: 8px 15px; border-radius: 20px; font-size: 0.9rem; cursor: pointer; transition: background-color 0.3s; }
                    .product-card button:hover { background-color: #ff9966; }
                    .added-text { color: green; font-weight: bold; display: none; }
                    .chat-btn { position: fixed; bottom: 20px; right: 20px; background-color: #ff5e62; border: none; border-radius: 50%; padding: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); cursor: pointer; z-index: 1000; }
                    .chat-window { display: none; position: fixed; bottom: 70px; right: 20px; width: 250px; border: 1px solid #ccc; border-radius: 8px; background-color: rgba(255, 255, 255, 0.3); backdrop-filter: blur(10px); box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); z-index: 1001; }
                    .chat-window textarea { background-color: rgba(255, 255, 255, 0.3); backdrop-filter: blur(10px);width: calc(100% - 50px); margin: 5px; padding: 5px; border-radius: 4px; border: 1px solid #ccc; }
                    .chat-window button { margin: 2px; padding: 8px 15px; border: none; background-color: #ff5e62; color: white; border-radius: 4px; cursor: pointer; }
                    footer { background-color: #333; color: white; text-align: center; padding: 10px; position: relative; bottom: 0; width: 96%; max-width:100%;}
                    .footer-icons { display: flex; justify-content: center; margin-top: 10px; }
                    .footer-icons i { color: #ff5e62; margin: 0 10px; }
                    @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,500;1,400&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
li {
  list-style: none;
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
}
.hamburger {
  display: block;
  cursor: pointer;
}

.bar {
  display: block;
  width: 25px;
  height: 3px;
  margin: 5px auto;
  transition: all 0.3s ease-in-out;
  background-color: #fff;
}

.nav-menu {
  position: fixed;
  top: 4.7rem;
  left: -100%;
  flex-direction: column;
  background-color: rgba(128, 145, 225, 0.3); backdrop-filter: blur(10px); border-top-right-radius: 15px; border-bottom-right-radius: 15px;
  font-size: 48px;
    color: #00BFFF;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    letter-spacing: 2px; 
  font-family: 'Georgia', serif;
  width: 230px;
  height: 600px;
  text-align: center;
  transition: 0.3s;
  box-shadow: 0 10px 27px rgba(0, 0, 0, 0.05);
}

.nav-menu.active {
  left: 0;
}

.nav-item {
  margin: 2.5rem 0;
}

.nav-link {
  font-size: 2rem;
  font-weight: 400;
  color: #fff;
}

.nav-link:hover {
  color: #482ff7;
}

.hamburger.active .bar:nth-child(2) {
  opacity: 0;
}

.hamburger.active .bar:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}

.hamburger.active .bar:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}
                </style>
            </head>
            <body>
                <nav class="navbar">
      <div class="hamburger">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">
          <a href="#" class="nav-link">Home</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link">About</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link">Projects</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link">Contact</a>
        </li>
      </ul>
                    <h2 style="color: white;">SNOWSHOP</h2>
                    <div>
                    <a href="#"><i class="fas fa-search"></i></a>
                    <a href="/cart"><i class="fas fa-shopping-cart"></i><span id="cart-count">0</span></a>
                    </div>
                </nav>
                <header>
                    <h1>Welcome to Our Store</h1>
                </header>
                <div class="product-section">
            """)

            # Render product cards dynamically
            for product in products:
                self.wfile.write(f"""
                    <div class="product-card">
                        <img src="{product['image']}" alt="{product['name']}">
                        <h2>{product['name']}</h2>
                        <p>${product['price']:.2f}</p>
                        <button onclick="addToCart({product['id']})">Add to Cart</button>
                        <span id="added-{product['id']}" class="added-text">Added ✔</span>
                    </div>
                """.encode())

            self.wfile.write(b"""
                </div>

                <footer>
                    <p>Fast Delivery <i class="fas fa-shipping-fast"></i></p>
                    <p>Great Products <i class="fas fa-star"></i></p>
                    <div class="footer-icons">
                        <a href="https://www.facebook.com" target="_blank"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.twitter.com" target="_blank"><i class="fab fa-twitter"></i></a>
                        <a href="https://www.instagram.com" target="_blank"><i class="fab fa-instagram"></i></a>
                    </div>
                </footer>

                <button class="chat-btn" onclick="toggleChat()"><i class="fas fa-comments"></i></button>

                <div class="chat-window" id="chat-window">
    <div id="chat-messages" style="max-height: 200px; overflow-y: auto; padding: 10px;"></div>
    <textarea id="chat-input" placeholder="Type your message..."></textarea>
    <button onclick="sendMessage()">Send</button>
</div>

                <script>
                    function addToCart(productId) {
                        fetch(`/add_to_cart?product_id=${productId}`)
                            .then(response => {
                                if (response.ok) {
                                    let addedElement = document.getElementById(`added-${productId}`);
                                    addedElement.style.display = 'inline';
                                    setTimeout(() => { addedElement.style.display = 'none'; }, 2000);
                                    
                                    let cartCount = document.getElementById('cart-count');
                                    cartCount.innerText = parseInt(cartCount.innerText) + 1;
                                } else {
                                    alert('Error adding product to cart.');
                                }
                            });
                    }

                    function toggleChat() {
                        var chatWindow = document.getElementById('chat-window');
                        chatWindow.style.display = chatWindow.style.display === 'none' || chatWindow.style.display === '' ? 'block' : 'none';
                    }

                    function sendMessage() {
    var input = document.getElementById('chat-input').value;
    if (input) {
        // Append user message to the chat window
        var chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML += `<div><strong>You:</strong> ${input}</div>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;  // Scroll to the bottom

        // Send message to the server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: input })
        })
        .then(response => response.json())
        .then(data => {
            // Append bot response to the chat window
            chatMessages.innerHTML += `<div><strong>SNOWSHOP:</strong> ${data.response}</div>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;  // Scroll to the bottom
        })
        .catch(error => console.error('Error:', error));

        // Clear the input field
        document.getElementById('chat-input').value = '';
    }
}
function toggleMenu() {
  const hamburger = document.querySelector(".hamburger");
  const navMenu = document.querySelector(".nav-menu");

  // Toggle active classes on both menu and hamburger icon
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
  });

  // Close menu on clicking any link
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      hamburger.classList.remove("active");
      navMenu.classList.remove("active");
    });
  });
}

// Initialize the toggle function
toggleMenu();
                </script>
            </body>
            </html>
            """)

        elif self.path.startswith("/add_to_cart"):
            # Handle adding product to the cart
            product_id = int(self.path.split('=')[1])
            if add_to_cart(product_id):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Product added to cart!")
            else:
                self.send_response(404)
                self.end_headers()

        elif self.path == "/cart":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            total = sum(product['price'] for product in cart)
            self.wfile.write(b"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Your Cart</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
                <style>
                    body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 0; color: #333; }
                    nav { display: flex; justify-content: space-between; align-items: center; background-color: #333; padding: 10px; }
                    nav a { color: #fff; text-decoration: none; padding: 5px 10px; font-size: 1rem; }
                    nav a:hover { color: #ff5e62; }
                    header { background: linear-gradient(45deg, #ff5e62, #ff9966); color: white; text-align: center; padding: 10px; }
                    header h1 { font-size: 2.5rem; margin: 0; }
                    .cart-section { padding: 20px; background-color: white; }
                    .cart-item { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #ddd; }
                    .cart-item:last-child { border-bottom: none; }
                    footer { background-color: #333; color: white; text-align: center; padding: 10px; position: relative; bottom: 0; width: 100%; }
                    .footer-icons { display: flex; justify-content: center; margin-top: 10px; }
                    .footer-icons i { color: #ff5e62; margin: 0 10px; }
                </style>
            </head>
            <body>
                <nav>
                    <h2 style="color: white;">SNOWSHOP</h2>
                    <a href="/"><i class="fas fa-home"></i> Home</a>
                </nav>
                <header>
                    <h1>Your Cart</h1>
                </header>
                <div class="cart-section">
            """)

            # Render cart items
            if cart:
                for item in cart:
                    self.wfile.write(f"""
                    <div class="cart-item">
                        <span>{item['name']}</span>
                        <span>${item['price']:.2f}</span>
                    </div>
                    """.encode())
            else:
                self.wfile.write(b"<p>Your cart is empty.</p>")

            self.wfile.write(f"""
                <h2>Total: ${total:.2f}</h2>
                <a href="/" style="display: inline-block; margin-top: 20px; padding: 10px; background-color: #ff5e62; color: white; border-radius: 5px; text-decoration: none;">Continue Shopping</a>
                </div>

                <footer>
                    <p>Fast Delivery <i class="fas fa-shipping-fast"></i></p>
                    <p>Great Products <i class="fas fa-star"></i></p>
                    <div class="footer-icons">
                        <a href="https://www.facebook.com" target="_blank"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.twitter.com" target="_blank"><i class="fab fa-twitter"></i></a>
                        <a href="https://www.instagram.com" target="_blank"><i class="fab fa-instagram"></i></a>
                    </div>
                </footer>
            </body>
            </html>
            """.encode())

        else:
            super().do_GET()

# Set up the server
PORT = 8000
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()