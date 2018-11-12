<html>
<head>
<style>
div {
    padding: 50px;
    border: 1px solid #4CAF50;
}
td, th {padding: 2px 15px 2px;
}
</style>
</head>
<body>
<div>
<h1>Lista de Plotagens Pendentes</h1>
% if len(protocolos) > 0:
	<p>Total de protocolos pendentes: {{ len(protocolos) }}</p>
	<table>
	<tr>
		<th>
			Data de envio
		</th>
		<th>
			Protocolo
		</th>
		<th>
			Login
		</th>
		<th>
			Tamanho da folha
		</th>
	</tr>
	% for protocolo in protocolos:
        	<tr>
			<td>
				{{ protocolo['data'] }} 
			</td>
			<td>
				{{ protocolo['protocolo'] }}
			</td>
			<td>
				{{ protocolo['login'] }}
			</td>
			<td>
				{{ protocolo['folha'] }}
			</td>
	    	</tr>	
	% end
	</table>
% else:
	<p>Nenhum protocolo encontrado.</p>
% end
<p>Atualizado em: {{atualizado}}</p>
</div>
</body>
</html>
