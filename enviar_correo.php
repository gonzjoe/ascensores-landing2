<?php
/**
 * Ascensores Wolf Group - Script de envío de formularios (v2.0)
 * Optimizado para servidores Apache/cPanel
 */

// --- CONFIGURACIÓN ---
$to = "info@ascensoreswolfgroup.com";
// Si no usas variables de entorno, puedes colocar tu clave secreta aquí:
$recaptcha_secret = getenv('RECAPTCHA_SECRET') ?: "6LcSjpMsAAAAAE8fI-Xm7t5-B9o7n6L5jH4G3F2D1"; // Reemplazar con la clave secreta real de Google

// Asegurar que recibimos la petición por POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Recibir los datos crudos
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    // Si no viene como JSON, tomar de $_POST
    if(!$data) {
        $data = $_POST;
    }
    
    $name = strip_tags(trim($data["name"] ?? ''));
    $email = filter_var(trim($data["email"] ?? ''), FILTER_SANITIZE_EMAIL);
    $phone = strip_tags(trim($data["phone"] ?? ''));
    $service = strip_tags(trim($data["service"] ?? ''));
    $message = strip_tags(trim($data["message"] ?? ''));
    $recaptcha_token = $data["recaptchaToken"] ?? '';

    // Validar reCAPTCHA
    if (empty($recaptcha_token)) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Validación de seguridad requerida."]);
        exit;
    }

    $verify = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret={$recaptcha_secret}&response={$recaptcha_token}");
    $response = json_decode($verify);

    // NOTA: Si tienes problemas con el reCAPTCHA en el servidor (ej. SSL) 
    // puedes comentar temporalmente este bloque if para pruebas.
    if (!$response->success || $response->score < 0.4) {
        http_response_code(403);
        echo json_encode(["status" => "error", "message" => "Error de verificación antispam. Reintente."]);
        exit;
    }

    // Comprobar campos obligatorios
    if (empty($name) || empty($message) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Por favor, complete todos los campos correctamente."]);
        exit;
    }

    // Construir el correo electrónico (HTML)
    $subject = "=?UTF-8?B?".base64_encode("Nueva solicitud web: $service")."?=";
    
    $email_html = "
    <html>
    <head>
        <style>
            body { font-family: sans-serif; line-height: 1.6; color: #333; }
            .container { padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            .header { background: #000; color: #fff; padding: 10px; text-align: center; border-radius: 5px 5px 0 0; }
            .content { padding: 20px; }
            .label { font-weight: bold; color: #005aa9; }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'><h2>Nueva solicitud de contacto</h2></div>
            <div class='content'>
                <p><span class='label'>Nombre:</span> $name</p>
                <p><span class='label'>Email:</span> $email</p>
                <p><span class='label'>Teléfono:</span> $phone</p>
                <p><span class='label'>Servicio:</span> $service</p>
                <p><span class='label'>Mensaje:</span><br>$message</p>
            </div>
        </div>
    </body>
    </html>";

    // Encabezados del correo para máxima compatibilidad con cPanel
    $headers = "MIME-Version: 1.0" . "\r\n";
    $headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
    // El 'From' DEBE ser un correo del dominio para que cPanel lo envíe
    $headers .= "From: Ascensores Wolf Group <info@ascensoreswolfgroup.com>" . "\r\n";
    $headers .= "Reply-To: $email" . "\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    // Enviar el correo
    if (mail($to, $subject, $email_html, $headers)) {
        http_response_code(200);
        echo json_encode(["status" => "success", "message" => "Mensaje enviado exitosamente. Nos contactaremos pronto."]);
    } else {
        http_response_code(500);
        echo json_encode(["status" => "error", "message" => "Error del servidor al procesar el envío."]);
    }

} else {
    http_response_code(403);
    echo "Metodo no permitido.";
}
?>
