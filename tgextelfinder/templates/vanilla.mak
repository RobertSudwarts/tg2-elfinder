<!DOCTYPE html>
<html>
<head>
  <meta charset="${response.charset}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>vanilla widget display</title>
</head>
<body>
<p> hello... anybody there ?? </p>
    ${ent_name}
    ${page}
    <hr/>
    ${tmpl_context.wdg.display() | n}

</body>
</html>

