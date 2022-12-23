## Adding This Extension
![Folders](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/ADD1.png)
![Folders](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/ADD2.png)
1. Download the package.
2. Go into the local address where you install Omniverse apps (code or create).
3. Just put the whole folder into "exts" or "extscache" folders where other extensions are installed. Both folders are OK.  



## Using This Extension
An exploded view is very useful to show the details of products in many fields like architecture and mechanical engineering... 
This extension provides an easy and reliable way to make exploded view in Omniverse.


### Step1: Match the formats
![Single Prim Format](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/FORMAT1.png)
![Parent Group Format](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/FORMAT2.png)
* Because of the core algorithm reads and manipulates the transform: translate and xformOp: translate: pivot attribute of prims,
before selecting, every single item needs to have a proper pivot coordinate around its geometric center, 
as well as the parent group if you want to choose it immediately. 
If the formats do not match, change the model in DCC, or directly change their properties if already imported in Omniverse.

### Step2: Create the Exploded Model
![Main Functions](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/MAIN1.png)
1. Select a group or all items at once and click the "Select Prims" button.
2. Change the X, Y, and Z ratio to control the explosion distance in different directions.
3. Change the coordinates of Pivot to control the explosion centre. 
* All items in the Exploded_Model will change dynamically with the change of X, Y, Z ratio and Pivot.

### Step3: Edit the Exploded Model
![Bind](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/EDIT1.png)
![Bind](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/EDIT2.png)
1. Select prims and click the "Add" or "Remove" button to add or remove them into or from the existed Exploded_Model. 
2. Select prims and click the "Bind" button if you want to keep the relative distances of selected items during explosion. 
3. Select a group and click the "Unbind" button to unleash their relative distances during explosion. 
* The Pivot of the Exploded_Model will change dynamically with adding or removing prims.

### Other Functions
![Axono](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/OTHER1.png)
![Axono](https://github.com/HC2ER/omniverse.tools.exploded_view/blob/master/docs/pics/OTHER2.png)
1. Click the "Axono" button and adjust the distance of the camera if you want an axonometric view.
2. Click the "Eye" button to hide or show the ORIGINAL prims.
3. Click the "Reset" button to reset the X, Y, Z ratio and Pivot.
4. Click the "Clear" button to delete the Exploded_Model.


### Future Development
* Add some animation functions to show the process of explosion.
* Improve the running speed and manipulation logic.

If you have any other questions about this extension, welcome to send the message or contact 460855381@qq.com.
