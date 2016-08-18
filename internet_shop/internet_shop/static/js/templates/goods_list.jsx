var template0 = (
	<div className="good">
		<img src={this.props.src} width='100'/>
		<input value={this.state.count} onChange={this.handleGoodCountChange} size='2'/>
			<button onClick={this.addGood}>
				Добавить в корзину
			</button>

		{ !this.state.exist ? <span class="error">Нету товара в таком количестве на складе</span>: null }
		<h6>{this.props.name}</h6>
		<span>Price - <strong>{this.props.price} $</strong></span>
	</div>
)