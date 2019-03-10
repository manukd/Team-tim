<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>





<body>
<?php
 echo "page api";
 // get the HTTP method, path and body of the request
$method = $_SERVER['REQUEST_METHOD'];
$request = explode('/', trim($_SERVER['PATH_INFO'],'/'));
$json = file_get_contents("php://input");
 

switch ($method) {

  case 'POST':
     echo "post reçu"; 
     echo $json;
     $maneuvre = "A droite";
     break;

}
?>
    <div class="container-fluid">
        <div class="row">
            <div class="col-lg-6">

            </div>
            <div class="col-lg-6">
                <div class="row">
                    
                    <div id="maneuvre"><?php $maneuvre ?></div>
                    <div id="distanceFinEtape"><?php $distanceFinEtape ?></div>
                    <div id="instruction"><?php $instruction ?></div>

                    <hr />

                    
                    <div id="kmRestant"><?php $kmRestant ?></div>
                    <div id="tempsRestant"><?php $tempsRestant ?></div>
                    <div id="adresseArrivee"><?php $adresseArrivee ?></div>                   

                </div>
            </div>
        </div>
    </div>
</body>
</html>
