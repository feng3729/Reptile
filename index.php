<?php

$mysql = mysql_connect("",'','') or die(mysql_error());
$mysql = mysql_select_db('gather') or die($myqsl->error());

$redis = new Redis();
$redis -> connect('127.0.0.1', 6379) or die('connect error');
$redis -> select(0);

$category = [
	'1' => 'xuanhuan',
	'2' => 'wuxia',
	'4' => 'dushi',
	'5' => 'junshi'
];

$param_arr = $argv;
$cate = htmlspecialchars_decode($param_arr['1']);
$cate = (int)urlencode($cate);
$cate = $cate ? $cate : 1;

$data = array();
// 设置来源
$referer = 'https://www.qisuu.la/';
// 设置IP
$header = array(
 // 'CLIENT-IP: 192.168.0.100',
 // 'X-FORWARDED-FOR: 192.168.0.100'
	'Accept: application/json',
	'Accept-Encoding: gzip'
);

function doCurl($url, $data=array(), $header=array(), $referer='',$timeout=3000)
{ 
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $header );
    curl_setopt($ch, CURLOPT_ENCODING , "gzip");
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
	curl_setopt($ch, CURLOPT_POST, true);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
	// curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch,CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11');
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);  //SSL 报错时使用
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);  //SSL 报错时使用
	curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);
	// 模拟来源
	curl_setopt($ch, CURLOPT_REFERER, $referer);
	$response = curl_exec($ch);
	if($error=curl_error($ch)){
		die($error);
	}
	curl_close($ch);
	return $response;
}


function doCon($maxpage=0,$redispage=0,$cate=1,$category='',$referer="",$data=[],$header=[])
{
	$forpage = $maxpage - $redispage;
	for($pid = 1;$pid <= $forpage;$pid++)
	{
		sleep(5);
		$url = 'https://www.qisuu.la/soft/sort0'.$cate.'/index_'.$pid.'.html';//外部采集网站
		$response = doCurl($url, $data, $header, $referer);
		preg_match_all("/作者：(.*?)<br \/>大小：([\.0-9MB]*?)<br>等级：<em class=\"lstar3\"><\/em><br>更新：(.*)?<\/div>\s*<a href=\"(.*?)\"><img src=\"(.*?)\" onerror=\"this.src='\/modules\/article\/images\/nocover.jpg'\">(.*?)<\/a>\s*<div class=\"u\">?(.*?)<\/div>\s*<div><a style=\"font-weight: normal;\" href=\"(.*?)\">最新章节：(.*?)<\/a><\/div>/",$response, $arr,PREG_SET_ORDER);
		for($i=0;$i<count($arr);$i++)
		{
			unset($arr[$i]['0']);
		}
		echo "\n\n采集第".$pid."页期望数据：\n\n";
		foreach ($arr as $k => $v)
		{
			$conStr = "https://www.qisuu.la".$v['4'];
			$conhtml = doCurl($conStr, $data, $header, $referer);
			preg_match_all("/<script type=\"text\/javascript\">get_down_url\(\'(.*?)\',\'(.*?)\',\'(.*?)\'\);<\/script>/",$conhtml, $downUrls,PREG_SET_ORDER);
			$downUrl = $downUrls['0']['2'];

			$sql = "insert into `cj_qishu_".$category."`(`title`,`author`,`desc`,`downUrl`,`thumb`,`size`,`updatetime`) values('{$v['6']}','{$v['1']}','{$v['7']}','{$downUrl}','https://www.qisuu.la{$v['5']}','{$v['2']}','{$v['3']}')";
			//需要执行的sql语句
			if((float)$v['2'] > 7.0)
			{
				$res=mysql_query($sql);
				if($res)
				{
					echo $v['6']."   作者：".$v['1']."   大小：".$v['2']."    下载链接为：".$downUrl."\n\n";
					
				}else{
					echo  "采集失败；ERROR：".mysql_error();
				}
			}
		}
	}
}


if(isset($category[$cate]))
{
	$url = 'https://www.qisuu.la/soft/sort0'.$cate.'/index_1.html';//外部采集网站
	$response = doCurl($url, $data, $header, $referer);
	preg_match_all("/\s<div class=\"tspage\">(.*?\/)([0-9]*)/ism",$response, $page,PREG_SET_ORDER);
	$maxpage = $page['0']['2'];
	$key = $category[$cate]."-maxpagelist";
	$redispage = $redis->get($key);
	if(!empty($redispage))
	{
		if($redispage < $maxpage)
		{
			$redis->set($key,$maxpage);
			doCon($maxpage,$redispage,$cate,$category[$cate],$referer);
		}else{
			die("\n\n过几天再来吧，他们的数据都已经被你爬完了！\n\n");
		}
	}else{
		$redis->set($key,$maxpage);
		doCon($maxpage,$redispage,$cate,$category[$cate],$referer);
	}
	
}else{
	die("\n你个坏蛋，想干嘛！\n\n");
}

mysql_close();
?>