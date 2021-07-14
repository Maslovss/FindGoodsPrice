const Pool = require('pg').Pool
const pool = new Pool({
  user: 'postgres',
  host: 'db',
  database: 'postgres',
  password: 'somePassword',
  port: 5432,
});

const getMerchants = () => {
  return new Promise(function(resolve, reject) {
    pool.query('SELECT topic1 , topic2 , topic3 , name , price , price_discount  FROM products limit 100', (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results.rows);
    })
  }) 
}



const getMerchantsByName = (merchantId) => {
  return new Promise(function(resolve, reject) {
    //const params_ =  '%' + merchantId + "%";
    var sql_ = "select topic1 , topic2 , topic3 , name , price , price_discount from products where ( 1 = 1) ";
    var params_ = new Array()
    if ( merchantId != "") {
        var splitted_array = merchantId.split(" ");
        for(var i = 1; i <= splitted_array.length ; i++) {
            sql_ = sql_ + " and ( LOWER(name) like $" + i.toString() +  " ) ";
            params_.push( "%" + splitted_array[i-1].toLowerCase() + "%");
        }
    }
    console.log("Filter = " + merchantId + "| Filter sql = " + sql_ + " | params = " + params_.toString() );

    pool.query(sql_ + " limit 100", params_ ,(error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results.rows);
    })
  }) 
}




const createMerchant = (body) => {
  return new Promise(function(resolve, reject) {
    const { name, email } = body

    pool.query('INSERT INTO products (name, email) VALUES ($1, $2) RETURNING *', [name, email], (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(`A new merchant has been added added: ${JSON.stringify(results.rows[0])}`)
    })
  })
}

const deleteMerchant = (merchantId) => {
  return new Promise(function(resolve, reject) {
    const id = parseInt(merchantId)

    pool.query('DELETE FROM products WHERE id = $1', [id], (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(`Merchant deleted with ID: ${id}`)
    })
  })
}

module.exports = {
  getMerchants,
  getMerchantsByName,  
  createMerchant,
  deleteMerchant,
}
