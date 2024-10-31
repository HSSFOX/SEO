<?php
//mima.php?action=update_mima&code=1234567890&userid=1&new_pwd=123456
define('PHPCMS_PATH', dirname(__FILE__).DIRECTORY_SEPARATOR);
include PHPCMS_PATH.'/topthink/base.php';
pc_base::load_sys_class('param','','','0');
$code = '1234567890'; // 安全密匙 请自行设置
if($_GET['code'] !== $code){
    showmessage('密匙不正确！！');
}
$action = $_GET['action'];
switch($action){
    case 'update_mima':
        $userid = intval($_GET['userid']);
        $new_pwd = trim($_GET['new_pwd']) ? trim($_GET['new_pwd']) : '123456';
        if($userid){
            $db = pc_base::load_model('admin_model');
            $data = $db->get_one("`userid`=$userid");
            if($data){
                $password = md5(md5($new_pwd).$data['encrypt']);
                $db->update("`password`='$password'", "`userid`=$userid");
                showmessage('密码初始化成功！！当前密码是'.$new_pwd, '/admin.php', 5000);
            }else{
                showmessage('管理员不存在！！');
            }
        }else{
            showmessage('参数错误！！');
        }

    break;
    default:

        showmessage('参数错误！！');
}

?>