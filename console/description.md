# QwenPaw Console 启动说明

本文说明在以下目录中如何启动前端开发服务，以及什么命令会打开 `8088` 端口。

```powershell
PS E:\Qcode\QwenPaw\console>
```

## 1. 哪个命令会打开 `8088`

会打开 `8088` 端口的是后端命令，不是前端命令：

```powershell
cd E:\Qcode\QwenPaw
python -m qwenpaw app
```

如果你的环境变量和命令安装都正常，也可以用：

```powershell
cd E:\Qcode\QwenPaw
qwenpaw app
```

启动成功后，可直接访问：

```text
http://127.0.0.1:8088/
```

说明：

- `8088` 是 QwenPaw 后端服务端口
- 后端也会托管构建后的控制台页面
- 如果你直接打开 `http://127.0.0.1:8088/agents`，也是走这套后端服务

## 2. 哪个命令会打开 `5173`

在 `console` 目录中运行下面命令，会启动 Vite 前端开发服务：

```powershell
cd E:\Qcode\QwenPaw\console
npm run dev
```

启动成功后，通常访问：

```text
http://127.0.0.1:5173/
```

说明：

- `5173` 是前端开发端口
- 适合改样式、改页面、看热更新
- `5173` 下的接口请求会代理到 `127.0.0.1:8088`
- 所以如果你只开了 `5173`，没开 `8088`，页面虽然能打开，但很多接口会报错

## 3. 推荐开发方式

如果你在改前端页面，推荐同时开两个终端。

终端 1：启动前端开发服务

```powershell
cd E:\Qcode\QwenPaw\console
npm run dev
```

终端 2：启动后端服务

```powershell
cd E:\Qcode\QwenPaw
python -m qwenpaw app
```

然后在浏览器中优先访问：

```text
http://127.0.0.1:5173/
```

这是最适合日常开发的方式，因为：

- 改前端代码后通常会自动刷新
- 后端接口也可正常联调
- 不需要每改一次都重新 build

## 4. 什么时候直接访问 `8088`

下面这些场景更适合直接访问 `8088`：

- 你想确认后端托管的正式页面是否正常
- 你不需要前端热更新
- 你想验证构建产物而不是 Vite 开发页

访问地址：

```text
http://127.0.0.1:8088/
```

注意：

- `8088` 展示的是后端托管的静态页面
- 它不会像 `5173` 一样自动反映最新源码改动
- 如果你改了前端源码，想让 `8088` 显示最新内容，通常需要重新构建

## 5. 如果想让 `8088` 显示最新前端改动

先构建前端：

```powershell
cd E:\Qcode\QwenPaw\console
npm run build
```

然后重启后端：

```powershell
cd E:\Qcode\QwenPaw
python -m qwenpaw app
```

当前项目里，后端会读取构建后的 `console/dist`。

## 6. 常用命令汇总

启动前端开发服务：

```powershell
cd E:\Qcode\QwenPaw\console
npm run dev
```

启动后端并打开 `8088`：

```powershell
cd E:\Qcode\QwenPaw
python -m qwenpaw app
```

构建前端：

```powershell
cd E:\Qcode\QwenPaw\console
npm run build
```

本地预览构建结果：

```powershell
cd E:\Qcode\QwenPaw\console
npm run preview
```

## 7. 一句话结论

如果你问“后续运行什么命令，会打开 `8088` 这个端口”，答案是：

```powershell
cd E:\Qcode\QwenPaw
python -m qwenpaw app
```

如果你只是改前端页面，推荐同时运行：

```powershell
cd E:\Qcode\QwenPaw\console
npm run dev
```

和

```powershell
cd E:\Qcode\QwenPaw
python -m qwenpaw app
```
