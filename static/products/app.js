var hostname = 'https://cycart-assignment.herokuapp.com/api/';
// var hostname = 'http://127.0.0.1:8000/api/';

const vm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    products: [],
    cart_data: []
  },
  mounted() {
    axios.get(hostname+"products/")
    .then(response => {this.products = response.data})

    axios.get(hostname+"cart/")
    .then(response => {this.cart_data = response.data})
  },
  methods: {
    add_product: function (product_id) {

     axios.post(hostname+"cart/", {
       "product_id": product_id
     })
    .then(response => {this.cart_data = response.data})

    },

    remove_product: function (product_id) {

     axios.put(hostname+"cart/", {
       "product_id": product_id,
       "action": "remove"
     })
    .then(response => {this.cart_data = response.data})

    },

    update_product: function (product_id, quantity) {

     axios.put(hostname+"cart/", {
       "product_id": product_id,
       "action": "update",
       "quantity": parseInt(quantity)
     })
    .then(response => {this.cart_data = response.data})

    }


  }
});
