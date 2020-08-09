const vm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    products: [],
    cart_data: []
  },
  mounted() {
    axios.get("http://127.0.0.1:8000/products/")
    .then(response => {this.products = response.data})

    axios.get("http://127.0.0.1:8000/cart/")
    .then(response => {this.cart_data = response.data})
  },
  methods: {
    add_product: function (product_id) {

     axios.post("http://127.0.0.1:8000/cart/", {
       "product_id": product_id
     })
    .then(response => {this.cart_data = response.data})

    },

    remove_product: function (product_id) {

     axios.put("http://127.0.0.1:8000/cart/", {
       "product_id": product_id,
       "action": "remove"
     })
    .then(response => {this.cart_data = response.data})

    },

    update_product: function (product_id, quantity) {

     axios.put("http://127.0.0.1:8000/cart/", {
       "product_id": product_id,
       "action": "update",
       "quantity": parseInt(quantity)
     })
    .then(response => {this.cart_data = response.data})

    }


  }
});
