<?php
/**
 * Compufield — Free Demo Class form handler
 *
 * Plain PHP, no plugins or outside services. Every demo request is emailed to
 * the addresses below using the server's built-in mail().
 *
 * To change who receives the leads, edit $TO.
 */

// ---------------------------------------------------------------------------
// Settings
// ---------------------------------------------------------------------------
$TO        = 'compufield@gmail.com, fkhairaz@gmail.com';
$FROM      = 'Compufield Website <noreply@compufield.com>'; // use an address on your own domain
$THANK_YOU = 'digital-marketing-thank-you.html';
$FALLBACK  = 'digital_marketing_course_mumbai.html';
$SAVE_COPY = true;   // also keep a copy of each request in demo-leads-backup.php (safety net if an email goes missing)
$BACKUP    = __DIR__ . '/demo-leads-backup.php';   // created automatically; opening it in a browser shows a blank page

$CENTRES = array('Kemps Corner (classroom)', 'Bandra West (classroom)', 'Live online');
$BATCHES = array('Weekday', 'Weekend', 'Fast-track', 'Not sure yet');

date_default_timezone_set('Asia/Kolkata');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function field($key, $max = 120) {
    $v = isset($_POST[$key]) ? (string) $_POST[$key] : '';
    $v = str_replace(array("\r", "\n", "%0a", "%0d"), ' ', $v);   // no header injection
    $v = trim(strip_tags($v));
    if (function_exists('mb_substr')) { return mb_substr($v, 0, $max, 'UTF-8'); }
    return substr($v, 0, $max);
}

function back_to($page, $why) {
    header('Location: ' . $page . '?demo=error&why=' . $why . '#demo', true, 303);
    exit;
}

// ---------------------------------------------------------------------------
// Only accept form posts
// ---------------------------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ' . $FALLBACK, true, 302);
    exit;
}

// Page the visitor came from (only our own .html files)
$page = basename(field('page', 100));
if (!preg_match('/^[a-z0-9_\-]+\.html$/i', $page) || !is_file(__DIR__ . '/' . $page)) {
    $page = $FALLBACK;
}

// ---------------------------------------------------------------------------
// Spam checks: hidden "website" field must be empty, and the form must have
// been open for at least 3 seconds (bots submit instantly).
// ---------------------------------------------------------------------------
if (field('website') !== '') {
    header('Location: ' . $THANK_YOU, true, 303);   // quietly drop bots
    exit;
}
$ts = (int) field('ts', 12);
if ($ts > 0 && (time() - $ts) < 3) {
    header('Location: ' . $THANK_YOU, true, 303);
    exit;
}

// ---------------------------------------------------------------------------
// Read and check the fields
// ---------------------------------------------------------------------------
$name   = field('name', 80);
$phone  = preg_replace('/[^0-9+]/', '', field('phone', 20));
$email  = field('email', 120);
$course = field('course', 90);
$centre = field('centre', 40);
$batch  = field('batch', 30);

$digits = preg_replace('/\D/', '', $phone);
if ($name === '' || strlen($digits) < 10 || strlen($digits) > 13) {
    back_to($page, 'fields');
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $email = '';
}
if (!in_array($centre, $CENTRES, true)) { $centre = 'Not specified'; }
if (!in_array($batch, $BATCHES, true))  { $batch = 'Not specified'; }
if ($course === '') { $course = 'Advanced Diploma in Digital Marketing with AI'; }

// WhatsApp link for the team to reply in one tap (Indian numbers get +91)
$wa = (strlen($digits) === 10) ? '91' . $digits : $digits;

// ---------------------------------------------------------------------------
// Build and send the email
// ---------------------------------------------------------------------------
$when = date('d M Y, h:i A');

$body  = "New FREE DEMO CLASS request from the website\n";
$body .= "==============================================\n\n";
$body .= "Name:      $name\n";
$body .= "Mobile:    $phone\n";
$body .= "Email:     " . ($email !== '' ? $email : '(not given)') . "\n";
$body .= "Course:    $course\n";
$body .= "Centre:    $centre\n";
$body .= "Batch:     $batch\n\n";
$body .= "Sent from: https://compufield.com/$page\n";
$body .= "Received:  $when (IST)\n\n";
$body .= "Reply on WhatsApp: https://wa.me/$wa\n";
$body .= "Call:              tel:$phone\n";

$subject = 'Free demo request: ' . $name . ' - ' . $course;
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$headers   = array();
$headers[] = 'From: ' . $FROM;
if ($email !== '') { $headers[] = 'Reply-To: ' . $name . ' <' . $email . '>'; }
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-Type: text/plain; charset=UTF-8';
$headers[] = 'X-Mailer: PHP/' . phpversion();

$sent = @mail($TO, $subject, $body, implode("\r\n", $headers));

// ---------------------------------------------------------------------------
// Keep a copy (optional)
// ---------------------------------------------------------------------------
$saved = false;
if ($SAVE_COPY) {
    // The first line stops PHP, so anyone opening this file in a browser sees a blank page.
    // Download it from cPanel File Manager / FTP to read it (it is plain CSV after line 1).
    $new = !is_file($BACKUP);
    $fh  = @fopen($BACKUP, 'a');
    if ($fh) {
        if ($new) {
            fwrite($fh, "<?php http_response_code(404); exit; ?>\n");
            fputcsv($fh, array('Received', 'Name', 'Mobile', 'Email', 'Course', 'Centre', 'Batch', 'Page', 'Emailed'));
        }
        $row = array($when, $name, $phone, $email, $course, $centre, $batch, $page, $sent ? 'yes' : 'NO');
        $row = str_replace(array('<?', '?>', '<%', '%>'), '', $row);
        fputcsv($fh, $row);
        fclose($fh);
        $saved = true;
    }
}

if ($sent || $saved) {
    header('Location: ' . $THANK_YOU, true, 303);
} else {
    back_to($page, 'send');
}
exit;
