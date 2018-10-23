<html>
<head>
</head>
<body>
<div>
<h1>Lista de Plotagens Pendentes</h1>
% if len(protocolos) > 0:
	<table>
	<tr>
		<th>
			Data de envio
		</th>
		<th>
			Protocolo
		</th>
		<th>
			Arquivo
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
				{{ protocolo['arquivo'] }}
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