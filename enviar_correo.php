<?php
// Configuración básica del correo
$to = "info@ascensoreswolfgroup.com";
$recaptcha_secret = "6LcSjpMsAAAAAOU8xmXniXQYOyY_kxfVQcSZQrKR"; // Clave secreta obtenida del usuario

// Asegurar que recibimos la petición por POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Recibir los datos crudos desde JSON o Form Data
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    // Si no viene como JSON, tomar de $_POST normal
    if(!$data) {
        $data = $_POST;
    }
    
    $name = strip_tags(trim($data["name"] ?? ''));
    $email = filter_var(trim($data["email"] ?? ''), FILTER_SANITIZE_EMAIL);
    $phone = strip_tags(trim($data["phone"] ?? ''));
    $service = strip_tags(trim($data["service"] ?? ''));
    $message = trim($data["message"] ?? '');
    $recaptcha_token = $data["recaptchaToken"] ?? '';

    // Validar reCAPTCHA
    if (empty($recaptcha_token)) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Falta la validación de reCAPTCHA."]);
        exit;
    }

    $verify_response = file_get_contents('https://www.google.com/recaptcha/api/siteverify?secret=' . $recaptcha_secret . '&response=' . $recaptcha_token);
    $response_data = json_decode($verify_response);

    if (!$response_data->success || $response_data->score < 0.5) {
        // Puntuación baja -> Es un bot
        http_response_code(403);
        echo json_encode(["status" => "error", "message" => "El sistema te detectó como posible bot de spam."]);
        exit;
    }

    // Comprobar campos obligatorios
    if (empty($name) || empty($message) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Completa todos los campos correctamente."]);
        exit;
    }

    // Construir el correo electrónico
    $subject = "Nuevo mensaje web - Servicio: $service (De: $name)";
    
    $email_content = "Has recibido una nueva solicitud a través de la página de contacto web:\n\n";
    $email_content .= "Nombre: $name\n";
    $email_content .= "Email: $email\n\n";
    $email_content .= "Teléfono: $phone\n";
    $email_content .= "Servicio solicitado: $service\n\n";
    $email_content .= "Mensaje:\n$message\n";

    // Encabezados del correo
    $headers = "From: webmaster@ascensoreswolfgroup.com\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    // Enviar el correo
    if (mail($to, $subject, $email_content, $headers)) {
        http_response_code(200);
        echo json_encode(["status" => "success", "message" => "Mensaje enviado exitosamente."]);
    } else {
        http_response_code(500);
        echo json_encode(["status" => "error", "message" => "Error interno al enviar el correo."]);
    }

} else {
    // Si la petición no es POST
    http_response_code(403);
    echo "Acceso denegado.";
}
?>
