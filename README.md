
<!---
This file is generated from automatically. (Any changes here will be overwritten)
--->
<p align="center">
    <a href="https://github.com/echo-lalia/Cardputer-MicroHydra" alt="MicroHydra">
        <img src="https://img.shields.io/badge/MicroHydra-purple" /></a>
 &nbsp;&nbsp;
    <a href="https://github.com/echo-lalia/microhydra-frozen" alt="MicroHydra Firmware">
        <img src="https://img.shields.io/badge/Firmware-purple" /></a>
  &nbsp;&nbsp;
    <a href="https://github.com/echo-lalia/Cardputer-MicroHydra/wiki" alt="Wiki">
        <img src="https://img.shields.io/badge/Wiki-slateblue" /></a>
</p>

# MicroHydra Apps!
This is a companion repository with a collection of community made apps for MicroHydra. 

<br/>


## Adding your apps to this repository:
If you've made an app compatible with MicroHydra, you can add it to this repository by submitting a pull request.

> This repo automatically generates `README.md` files *(and more)* using the scripts under `/tools`.  
> For this to work, your app needs to be placed into the `app-source` directory, following the same general format as the apps around it.

*Here are step-by-step instructions for how you can add an app:*
- [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) this repository on your own account

- Add a directory specifically for your app to the `app-source` directory

- Place your app in that directory by uploading, or by adding your own repo as a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules)  
  *(Either the `.py` file, or the entire folder containing your `__init__.py` should be added)*

- Create a `details.yml` file alongside your app. This should contain your name, a description, license, and specify the target device(s)  
  *(See [`app-source/default.yml`](https://github.com/echo-lalia/MicroHydra-Apps/blob/main/app-source/default.yml), or the other uploaded apps for the format used here)*

- Submit a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) to this repo with your changes.

<br/>

For clarity, this is how the `app-source` folder is structured:

*app-source/*    
├── ***myUniqueAppName/***  
│ &nbsp; &nbsp; &nbsp; ├── **myApp.py**  
│ &nbsp; &nbsp; &nbsp; └── **details.yml**  
│  
├── ***thisNameInRepo/***  
│ &nbsp; &nbsp; &nbsp; ├── ***thisNameInMicroHydra/***  
│ &nbsp; &nbsp; &nbsp; │ &nbsp; &nbsp; &nbsp; ├── icon.raw  
│ &nbsp; &nbsp; &nbsp; │ &nbsp; &nbsp; &nbsp; ├── someotherappfile.py  
│ &nbsp; &nbsp; &nbsp; │ &nbsp; &nbsp; &nbsp; └── \_\_init\_\_.py    
│ &nbsp; &nbsp; &nbsp; └── **details.yml**  
│  
└── default.yml  



<br/><br/>


# Apps by device:  

*This repo currently hosts **2** apps, for **1** unique devices, by **2** different authors.*  
*Click a link below to jump to the apps for that specific device.*

- [Cardputer](#cardputer)


<br/><br/><br/>        

## Cardputer  
*There are 2 apps for the Cardputer.*


### <img src="images/icons/InfraRed.png" width="14"> [InfraRed](https://github.com/echo-lalia/MicroHydra-Apps/tree/main/app-source/InfraRed)  
> <img src="https://github.com/ndrnmnk.png?size=20" width="10"> **[ndrnmnk](https://github.com/ndrnmnk)**  
> Version: **1.0** | License: **?**  
> Infrared codes sender/reciever app. v21
<br/>

### <img src="images/icons/Remote.png" width="14"> [Remote](https://github.com/echo-lalia/MicroHydra-Apps/tree/main/app-source/Remote)  
> <img src="https://github.com/echo-lalia.png?size=20" width="10"> **[Luccas](https://github.com/echo-lalia)**  
> Version: **1.1** | License: **[MIT](https://github.com/echo-lalia/MicroHydra-Apps/blob/main/LICENSE)**  
> Luccas' remote for his TV 1.0
<br/>

