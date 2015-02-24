Design questions about the package
====

* **Relocating methods of Google class in separated modules** Encapsulate the logic and functions of each kind of search method outside the public class used by the user to be able to maintain them and repair them without touching the main module and interface. (More maintainable or overkilling?)

* **Duplicated docstrings between methods in the main class and methods in the modules** Updates in main module docstrings should be followed by duplicated updates in auxiliary modules docstrings. (should I put docstrings only in the main module?)

* **Private methods "floating" in a module as global methods** It feels uncomfortable to have private methods not wrapped into a class, but adding classes inside auxiliary methods complicates the interface of the modules unnecessarily (should I keep them like this? Without "wrapping" classes?)

* **Order of methods in the modules** Private methods before public methods or vice-versa? First approach shows first the bricks of the wall and then the wall, second approach shows first what the user can use about the module and "hide" some implementation details.

* **Top down approach in currency: overkilling?** How far would be desirable to go in breaking down public methods into private ones to make more clear the algorithm followed by the main public method?

* **Closely related tests between main module and auxiliary modules** Some tests in the google module seems to test just the same than some tests in the auxiliary modules. At some point this is duplicating code and work (specially when test must be changed) but they respond to different compartments of the package.

* **Is it ok to upload something so informal as these DESIGN_QUESTIONS to github?** Transparency vs. overpopulate the package??