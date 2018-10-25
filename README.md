# medMetric
A script to compute metrics for medical images based on some public libraries. Since it seems that it can only process the binary volumes, I write a wrapper to make it be able to work on mulpitle category volumes. I also made some subtle changes to the surface-distance computation which is not quite deterministic in original version. I will publish my own core metric computational libraries later (I'm now checking them to make sure they are correct).

I suppose you have installed:    <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ubuntu 16.04
     <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;simpleITK 
     <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;numpy
     <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;gcc 4.8+<br>
The following should be better installed, but not nessary if you donot directly use the binary copy of EvaluationSegmentation library I provided:
     <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ITV
     <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;VTK
     <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CMAKE


if you want to test the functions, you can use <a href='https://github.com/abseil/abseil-py'>absltest</a> to write a simple test unit.

In this copy of codes, we have referred to https://github.com/Visceral-Project/EvaluateSegmentation and https://github.com/deepmind/surface-distance (the core metric computational lib is from these two copies in this current reporistory).
