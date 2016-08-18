var Good = React.createClass({
	getInitialState: function () {
		return { 
			count: this.props.type_template == 1 ? this.props.count: 1, 
			price: this.props.price, 
			id: this.props.id, 
			exist: this.props.type_template == 2 ? this.props.exist: true, 
			sum: parseInt(this.props.count) * parseInt(this.props.price) 
		};
    },

	handleGoodCountChange: function(e) {
	    this.setState({
	    	count: e.target.value
	    }, function() {
	    	this.checkExist();
	    });
	},

	addGood: function() {
		$.post('/cart/add/', {
			id:this.props.id,
			count: this.state.count,
		}, function(response) {
			if (parseInt(response) == 1)
				var enable = true;
			else
				var enable = false;
			this.setExist(enable);
		}.bind(this));
	},

	setExist: function(enable) {
		this.setState({
			exist: enable,
		})
	},

	setSum: function(e) {
		this.setState({
			count: parseInt(e.target.value),
		}, function() {
			this.checkExist();
			this.getSum();
		})
	},

	getSum:function() {
		if (this.state && this.state.count && this.state.price) {
			this.props.update(this.state);
			return this.state.count * this.state.price;
		}
		else
			return 0;
	},

	remove: function() {
		this.props.remove(this.state.id);
	},

	checkExist: function() {
		$.get('/good/exist/' + this.state.id + "/?count=" + this.state.count, function(res) {
			if (parseInt(res))
				var enable = true;
			else
				var enable = false;
			this.setExist(enable);
		}.bind(this));
	},

	setExist: function(enable) {
		this.setState({
			exist: enable,
		})
	},

	render: function() {
		if (this.props.type_template == 0) {
			return (
				<div className="form-group">
					<img src={this.props.src} width='100'/>
					<div className="col-xs-1">
						<label for="good_count">count:</label>
						<input value={this.state.count} type="number" id="good_count" className="form-control" onChange={this.handleGoodCountChange}/>
					</div>

					<div className="form-group">
						<h4>{this.props.name}</h4>
						<div class="pull-right">Price - <span className="badge">{this.props.price} $</span></div>
					</div>
					<button onClick={this.addGood} className="btn btn-success">
						Добавить в корзину
					</button>
					{ !this.state.exist ?  <div className="alert alert-warning" role="alert">
						<span class="error">Нету товара в таком количестве на складе</span>
					</div>: null }
				</div>
			)
		}
		else if (this.props.type_template == 1){
			return (
				<div className="form-group m-b-40">
					<img src={this.props.src} width='100'/>
					<div className="col-xs-1">
						<label for="good_count">count:</label>
						<input type="number" value={this.state.count} id="good_count" className="form-control" onChange={this.handleGoodCountChange}/>
					</div>

					<div className="form-group">
						<h4>{this.props.name}</h4>
						<div class="pull-right">Сумма - <span className="badge">{this.getSum()} $</span></div>
					</div>

					<button onClick={this.props.remove.bind(this, this.props.id)} className="btn btn-danger">Удалить</button>

					{ !this.state.exist ?  <div className="alert alert-warning" role="alert">
						<span class="error">Нету товара в таком количестве на складе</span>
					</div>: null }
				</div>
			)
		}
		else if (this.props.type_template == 2) {
			return (
				<div className="form-group m-b-40">
					<img src={this.props.src} width='100'/>
					
					<div className="form-inline">

						<div className="form-group">
							<div>Количество товара - <span className="badge">{this.props.count}</span></div>
							<h4>{this.props.name}</h4>
							<div>Стоимость - <span className="badge">{this.state.sum} $</span></div>
						</div>
						<div className="form-group">
							{ !this.state.exist ?  <div className="alert alert-warning" role="alert">
								<span class="error">Нету товара в таком количестве на складе</span>
							</div>: null }

						</div>
					</div>
				</div>
			)
		}
	}
})

status = {
	0: "Ошибка",
	1: "Успешно",
	2: "Товара нет в наличии",
}

var Pay = React.createClass({
	getInitialState: function() {
	    return {
	          goods: [],
	          card_number: "",
	          payment_system: 1,
	    };
	},

	componentDidMount: function() {
		$.get('/cart/get/', function(response) {
			if (this.isMounted()) {
				var data = JSON.parse(response);
				this.setState({
					goods: data.goods,
					payment_system: data.payment_system,
				});
			}
		}.bind(this));
	},

	pay: function() {
		if (this.state.card_number.length == 16)
			$.post('/cart/pay/', {
				card_number: this.state.card_number, 
			}, function(response) {
				alert(status[response]);
			})
	},

	getFullPrice: function() {
		var price = 0;
		this.state.goods.forEach(function(elem) {
			price += parseInt(elem.price) * parseInt(elem.count);
		})
		return price;
	},

	setCardNumber: function(e) {
		this.setState({
			card_number: e.target.value,
		})
	},

	render: function() {
		var goods = this.state.goods.map(function(good) {
	    	return <Good src={good.photo} name={good.name} price={good.price} id={good.id} count={good.count} exist={good.exists} type_template={2}/>
	    });

	    return (
		    <div>
		    	<nav className="navbar navbar-default">
  					<div className="container-fluid">
  						<div className="navbar-collapse" id="bs-example-navbar-collapse-1">
				    		<ul className="nav navbar-nav navbar-right">
				      			<li><ReactRouter.Link to='/cart'>Вернуться в корзину</ReactRouter.Link></li>
				      		</ul>
				      	</div>
			      	</div>
		    	</nav>

		        {goods}

		        <div className="form-group">
		    		<div>Полная стоимость - <span className="badge">{this.getFullPrice()} $</span></div>
		    	</div>

		    	<div className="form-group">
		    		<span>Платежная система - </span>
		    		<span id="payment_system"><strong>{this.state.payment_system.name}</strong></span>
		    	</div>

		        <div className="form-group">
					<div className="col-xs-2">
			      		<label for="card_number">Номер карты</label>
			      		<input className="form-control"  id="card_number" placeholder="16-ти значный номер" onChange={this.setCardNumber}/>
			      	</div>

					<div className="">
		     			<button type="button" className="btn btn-primary m-t-25" onClick={this.pay}>Оплатить</button>
			     	</div>		    
		     	</div>		    
		    </div>
		    )
	},
})

var AllGoods = React.createClass({
	getInitialState: function() {
		return {
			all_goods: [],
			cart: [],
		}
	},

	componentDidMount: function() {
		$.get('/good/all/', function(response) {
			if (this.isMounted()) {
				this.setState({
					all_goods: JSON.parse(response),
				});
			}
		}.bind(this));
	},

	render: function() {
		if (this.state.all_goods) {
			var parent_this = this;
		    var goods = this.state.all_goods.map(function(good) {
		      return <Good src={good.photo} name={good.name} price={good.price} id={good.id} type_template={0}/>
		    });

		    return (
		    <div>
		    	<nav className="navbar navbar-default">
  					<div className="container-fluid">
  						<div className="navbar-collapse" id="bs-example-navbar-collapse-1">
				    		<ul className="nav navbar-nav navbar-right">
				      			<li><ReactRouter.Link to='/cart'>Перейти в корзину</ReactRouter.Link></li>
				      		</ul>
				      	</div>
			      	</div>
		    	</nav>
		        {goods}
		    </div>
		    )
		}
	}
})


var Cart = React.createClass({
	getInitialState: function () {
		return { goods: [], full_price: this.getFullPrice(), pay_systems: [], optionsState: 1 };
    },

	componentDidMount: function() {
		$.get('/cart/get/', function(response) {
			if (this.isMounted()) {
				var data = JSON.parse(response);
				this.setState({
					goods: data.goods,
					optionsState: data.payment_system.id,
				});
			}
		}.bind(this));
		$.get('/cart/pay-systems/', function(response) {
			var options = [];
			var pay_systems = JSON.parse(response);

			for (var elem in pay_systems) 
				options.push({ value: parseInt(elem), label: pay_systems[elem]});

			if (this.isMounted()) {
				this.setState({
					options: options,
					pay_systems: pay_systems,
				});
			}
		}.bind(this));
	},

	setChangeData: function(data) {
		this.state.goods.map(function(elem) {
			if (elem.id == data.id)
				elem.count = data.count;
		})
		this.getFullPrice();
	},

	getFullPrice: function() {
		var price = 0;
		if (this.state) {
			this.state.goods.map(function(good) {
				price += good.price * good.count;
			})
		}

		if (this.isMounted() && this.state.full_price != price) {
			this.setState({
				full_price: price,
			});
		}
	},

	removeGood: function(id) {
		this.state.goods.map(function(good, i) {
			if (good.id == id) {
				delete this.state.goods[i];

				$.post('/cart/remove/',	{ id: id })

				this.setState({
					goods: this.state.goods,	
				});

				this.getFullPrice();
			}
		}, this);
	},

	confirmCart: function() {
		var pay_data = [];
		var goods = this.state.goods;
		for (var i in goods)
			pay_data.push({
				'id': goods[i].id,
				'count': goods[i].count,
			})

		$.post('/cart/confirm-cart/', {
			goods: pay_data,
			pay_system: this.state.optionsState,
		}, function(response) {
			
		}.bind(this))
	},

	changePaySystem: function(inputValue) {
		this.setState({
			optionsState: parseInt(inputValue.value),
		});
	},

	render: function() {
		if (this.state.goods.length) {
			var parent_this = this;
			var goods = this.state.goods.map(function(good) {
				return (
					<Good src={good.photo} 
						count={good.count} 
						price={good.price} 
						update={parent_this.setChangeData} 
						id={good.id} 
						remove={parent_this.removeGood} 
						type_template={1}/>
				)
			})

			return (
				<div>
					<nav className="navbar navbar-default">
	  					<div className="container-fluid">
	  						<div className="navbar-collapse" id="bs-example-navbar-collapse-1">
					    		<ul className="nav navbar-nav navbar-right">
					      			<li><ReactRouter.Link to='/pay' onClick={this.confirmCart}>Оплатить</ReactRouter.Link></li>
					      			<li><ReactRouter.Link to='/'>Вернуться к списку товаров</ReactRouter.Link></li>
					      		</ul>
					      	</div>
				      	</div>
			    	</nav>
			        {goods}
			        <div className="form-group">
				        <label for="payment_system">Payment system</label>
				        <Select
				        	id="payment_system"
						    name="form-field-name"
						    value={this.state.optionsState}
						    options={this.state.options}
						    onChange={this.changePaySystem}
						/>
				    </div>
		      </div>
		    )
		}
		return (<div></div>)
	}
})


ReactDOM.render((
  <ReactRouter.Router>
    <ReactRouter.Route path="/" component={AllGoods}>
    </ReactRouter.Route>

    <ReactRouter.Route path="cart" component={Cart}/>
    <ReactRouter.Route path="pay" component={Pay}/>
  </ReactRouter.Router>
), document.body);


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
                  );
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    }
});