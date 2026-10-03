[[ PAGE 1 ]]
BEGINNING EXCEL
NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE
SHINGLEDECKER
Open Oregon Educational Resources
[[ PAGE 2 ]]
This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by/4.0/.
Beginning Excel by Noreen Brown, Barbara Lave, Julie Romey, Mary Schatz, Diane Shingledecker is licensed under a Creative
Commons Attribution 4.0 International License, except where otherwise noted.
[[ PAGE 3 ]]
CONTENTS
CHAPTER 1 - FUNDAMENTAL SKILLS
CHAPTER 2 - MATHEMATICAL COMPUTATIONS
CHAPTER 3 - FORMULAS, FUNCTIONS, LOGICAL AND LOOKUP FUNCTIONS
CHAPTER 4 - PRESENTING DATA WITH CHARTS
4.1 Choosing a Chart Type
9
4.2 Formatting Charts
39
4.3 Using Charts with Microsoft® Word® and Microsoft® PowerPoint®
60
4.4 Preparing to Print
69
4.5 Chapter Practice
75
4.6 Scored Assessment
78
CHAPTER 5 - TABLES
CHAPTER 6 - MULTIPLE SHEET FILES
[[ PAGE 4 ]]
[[ PAGE 5 ]]
CHAPTER 1 - FUNDAMENTAL SKILLS
Microsoft® Excel® is a tool that can be used in virtually all careers and is valuable in both professional
and personal settings. Whether you need to keep track of medications in inventory for a hospital or
create a financial plan for your retirement, Excel enables you to do these activities efficiently and
accurately. This chapter introduces the fundamental skills necessary to get you started in using Excel.
You will find that just a few skills can make you very productive in a short period of time.
ATTRIBUTION
Adapted from How to Use Microsoft Excel: The Careers in Practice Series, adapted by The Saylor
Foundation without attribution as requested by the work’s original creator or licensee, and licensed
under CC BY-NC-SA 3.0.
[[ PAGE 6 ]]
[[ PAGE 7 ]]
CHAPTER 2 - MATHEMATICAL COMPUTATIONS
Perhaps the most valuable feature of Excel is its ability to produce mathematical outputs using the
data in a workbook. This chapter reviews several mathematical outputs that you can produce in Excel
through the construction of formulas and functions. The chapter begins with the construction of
formulas for basic and complex mathematical computations. The second section reviews statistical
functions, such as SUM, AVERAGE, MIN, and MAX, which can be applied to a range of cells. The last
section of the chapter addresses functions used to calculate mortgage and lease payments as well as
the valuation of investments. This chapter also shows how you can use data from multiple worksheets
to construct formulas and functions. These skills will be demonstrated in the context of a personal
cash budget, which is a vital tool for managing your money for long-term financial security. The
personal budget objective will also provide you with several opportunities to demonstrate Excel’s
what-if scenario capabilities, which highlight how formulas and functions automatically produce new
outputs when one or more inputs are changed.
ATTRIBUTION
Adapted by Mary Schatz from How to Use Microsoft Excel: The Careers in Practice Series, adapted
by The Saylor Foundation without attribution as requested by the work’s original creator or
licensee, and licensed under CC BY-NC-SA 3.0.
[[ PAGE 8 ]]
[[ PAGE 9 ]]
CHAPTER 3 - FORMULAS, FUNCTIONS, LOGICAL
AND LOOKUP FUNCTIONS
Excel workbooks are designed to allow you to create useful and complex calculations. In addition to
doing arithmetic, you can use Excel to look up data, and to display results based on logical conditions.
We will also look at ways to highlight specific results. These skills will be demonstrated in the context
of a typical gradebook spreadsheet that contains the results for an imaginary Excel class.
In this chapter, we will:
• Use the Quick Analysis Tool to find the Total Points for all students and Points Possible.
• Write a division formula to find the Percentage for each student, using an absolute reference to the
Total Points Possible.
• Write an IF Function to determine Pass/Fail – passing is 70% or higher.
• Write a VLOOKUP to determine the Letter Grade using the Letter Grades scale.
• Use the TODAY function to insert the current date.
• Review common Error Messages using Smart Lookup to get definitions of some of the terms in
your spreadsheet.
• Apply Data Bars to the Total Points values.
• Apply Conditional Formatting to the Percentage, Pass/Fail, and Letter Grade columns.
• Printing Review – Change to Landscape, Scale to Fit Columns on One Page and Set Print Area.
Figure 3-1 shows the completed workbook that will be demonstrated in this chapter. Notice the
techniques used in columns O and R that highlight the results of your calculations. Notice, also that
there are more numbers on this version of the file than you will see in your original data file. These
are all completed using Excel calculations.
Figure 3.1 Completed Gradebook Worksheet
[[ PAGE 10 ]]
ATTRIBUTION
Chapter 3 – Formulas, Functions, Logical and Lookup Functions by Noreen Brown and Mary Schatz,
Portland Community College, is licensed under CC BY 4.0
[[ PAGE 11 ]]
CHAPTER 4 - PRESENTING DATA WITH CHARTS
One of the most important things to consider when using charts in Excel is that they are intended
to be used for communicating an idea to an audience. Your audience can be reading your charts in a
written document or listening to you in a live presentation. In fact, Excel charts are often imported or
pasted into Word documents or PowerPoint slides, which serve this very purpose of communicating
ideas to an audience. Although there are no rules set in stone for using specific charts for certain
data types, some chart types are designed to communicate certain messages better than others. This
chapter explores numerous charts that can be used for a variety of purposes. In addition, we will
examine formatting charts and using those charts in Word and PowerPoint documents.
ATTRIBUTION
Adapted by Noreen Brown from How to Use Microsoft Excel: The Careers in Practice Series, adapted
by The Saylor Foundation without attribution as requested by the work’s original creator or
licensee, and licensed under CC BY-NC-SA 3.0.
[[ PAGE 12 ]]
[[ PAGE 13 ]]
4.1 CHOOSING A CHART TYPE
LEARNING OBJECTIVES
1.
Construct a line chart to show a time series trend.
2.
Learn how to adjust the Y axis scale.
3.
Construct a line chart to present a comparison of two trends.
4.
Learn how to use a column chart to show a frequency distribution.
5.
Create a separate chart sheet for a chart embedded in a worksheet.
6.
Construct a column chart that compares two frequency distributions.
7.
Learn how to use a pie chart to show the percent of total for a data set.
8.
Construct a stacked column chart to show how a percent of total changes over time.
This section reviews the most commonly used Excel chart types. To demonstrate the variety of chart
types available in Excel, it is necessary to use a variety of data sets. This is necessary not only to
demonstrate the construction of charts but also to explain how to choose the right type of chart given
your data and the idea you intend to communicate.
CHOOSING A CHART TYPE
Before we begin, let’s review a few key points you need to consider before creating any chart in Excel.
1. The first is identifying your idea or message. It is important to keep in mind that the primary
purpose of a chart is to present quantitative information to an audience. Therefore, you must
first decide what message or idea you wish to present. This is critical in helping you select
specific data from a worksheet that will be used in a chart. Throughout this chapter, we will
reinforce the intended message first before creating each chart.
2. The second key point is selecting the right chart type. The chart type you select will depend
on the data you have and the message you intend to communicate.
3. The third key point is identifying the values that should appear on the X and Y axes. One of
the ways to identify which values belong on the X and Y axes is to sketch the chart on paper
first. If you can visualize what your chart is supposed to look like, you will have an easier time
selecting information correctly and using Excel to construct an effective chart that accurately
communicates your message. Table 4.1 “Key Steps Before Constructing an Excel Chart”
provides a brief summary of these points.
BEGINNING EXCEL 9
[[ PAGE 14 ]]
Table 4.1 Key Steps before Constructing an Excel Chart
Step
Description
Define your
message.
Identify the main idea you are trying to communicate to an audience. If there is no main point or important
message that can be revealed by a chart, you might want to question the necessity of creating a chart.
Identify the data
you need.
Once you have a clear message, identify the data on a worksheet that you will need to construct a chart. In
some cases, you may need to create formulas or consolidate items into broader categories.
Select a chart type.
The type of chart you select will depend on the message you are communicating and the data you are using.
Identify the values
for the X and Y
axes.
After you have selected a chart type, you may find that drawing a sketch is helpful in identifying which
values should be on the X and Y axes. In Excel, the axes are:
The “category” axis. Usually the horizontal axis – where the labels are found
The “value” axis. Usually the vertical axis – where the numbers are found.
TIME SERIES TREND: LINE CHART 1
The first chart we will demonstrate is a line chart. Figure 4.1 shows part of the data that will be used
to create two line charts. This chart will show the trend of the NASDAQ stock index.
Read more: http://www.investopedia.com/terms/n/nasdaq.asp
This chart will be used to communicate a simple message: to show how the index has performed over
a two-year period. We can use this chart in a presentation to show whether stock prices have been
increasing, decreasing, or remaining constant over the designated period of time.
Integrity Check
Carefully Select Data When Creating a Chart
Just because you have data in a worksheet does not mean it must all be placed onto a chart. When creating a chart,
it is common for only specific data points to be used. To determine what data should be used when creating a chart,
you must first identify the message or idea that you want to communicate to an audience.
10 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 15 ]]
Figure 4.1 Stock Trends
Before we create the line chart, it is important to identify why it is an appropriate chart type given the
message we wish to communicate and the data we have. When presenting the trend for any data over
a designated period of time, the most commonly used chart types are the line chart and the column
chart. With the column chart, you are limited to a certain number of bars or data points. As you
increase the number of bars on a column chart, it becomes increasingly difficult to read. As you scroll
through the data on the worksheet shown in Figure 4.1 you will see that there are 24 points of data
used to construct the chart. This is generally too many data points to put on a column chart, which is
why we are using a line chart. Our line chart will show the volume of sales for the NASDAQ on the Y
axis and the Month number on the X axis. The following steps explain how to construct this chart:
Download Data file: CH4 Data
1. Open data file CH4 Data and save a file to your computer as CH4 Charting.
2. Navigate to the Stock Trend worksheet.
3. Highlight the range B4:C28 on the Stock Trend worksheet. (Note – you have selected a label in
the first row and more labels in column B. Watch where they show up in your completed chart.)
4. Click the Insert tab of the ribbon.
5. Click the Line button in the Charts group of commands. Click the first option from the list,
which is a basic 2D Line Chart (see Figure 4.2).
BEGINNING EXCEL 11
[[ PAGE 16 ]]
Figure 4.2 Selecting the Basic Line Chart
This adds, or embeds, the line chart to the worksheet, as shown in Figure 4.3
Figure 4.3 shows the embedded line chart in the Stock Trend worksheet. Do you see where your labels
showed up on the chart?
Why?
Line Chart vs. Column Chart
We can use both a line chart and a column chart to illustrate a trend over time. However, a line chart is far more
effective when there are many periods of time being measured. For example, if we are measuring fifty-two weeks,
a column chart would require fifty-two bars. A general rule of thumb is to use a column chart when twenty bars or
less are required. A column chart becomes difficult to read as the number of bars exceeds twenty.
12 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 17 ]]
Notice that additional tabs, or contextual tabs, are added to the ribbon. We will demonstrate the
commands in these tabs throughout this chapter. These tabs appear only when the chart is activated.
Figure 4.3 Embedded Line Chart in the Stock Trend Worksheet
As shown in Figure 4.3, the embedded chart is not placed in an ideal location on the worksheet
since it is covering several cell locations that contain data. The following steps demonstrate common
adjustments that are made when working with embedded charts:
1. Moving a chart: Click and drag the upper left corner of the chart to the center of cell B30.
2. Resizing a chart: Place the mouse pointer over the right upper corner sizing handle, hold down
the ALT key on your keyboard, and click and drag the chart so it “snaps” to the right side of
Column I.
3. Repeat step 2 to resize the chart so the top “snaps” to the top of Row 30, the bottom “snaps” to
Note: Excel 2010 uses three contextual tabs for charts. Later versions use only two. Each has all the
same tools. They are just organized a little differently.
BEGINNING EXCEL 13
[[ PAGE 18 ]]
the bottom of Row 45, and the left side “snaps” to the left side of Column B. Make sure the right
side of the chart snaps to the line between column I and J.
4. Adjusting the chart title: Click the chart title once. Then click in front of the first letter. You
should see a blinking cursor in front of the letter. This allows you to modify the title of the chart.
5. Type the following in front of the first letter in the chart title: May 2014-2016 Trend for
NASDAQ Sales.
6. Click anywhere outside of the chart to deactivate it.
7. Save your work.
Figure 4.4 shows the line chart after it is moved and resized. You can also see that the title of the
chart has been edited to read May 2014-2016 Trend for NASDAQ Sales Volume. Notice that the
sizing handles do not appear around the perimeter of the chart. This is because the chart has been
deactivated. To activate the chart, click anywhere inside the chart perimeter.
Note: Keep an eye on your pointer. It will change into
when you are in the right place to move your
chart.
Note: keep an eye on your pointer. It will change into
when you are in the right place to resize your
chart
14 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 19 ]]
Figure 4.4 Line Chart Moved and Resized
Skill Refresher
Inserting a Line Chart
Integrity Check
When using line charts in Excel, keep in mind that anything placed on the X axis is considered a descriptive label,
not a numeric value. This is an example of a category axis. This is important because there will never be a change in
the spacing of any items placed on the X axis of a line chart. If you need to create a chart using numeric data on the
category axis, you will have to modify the chart. We will do that later in the chapter.
BEGINNING EXCEL 15
[[ PAGE 20 ]]
1.
Highlight a range of cells that contain data that will be used to create the chart. Be sure to include labels
in your selection.
2.
Click the Insert tab of the ribbon.
3.
Click the Line button in the Charts group.
4.
Select a format option from the Line Chart drop-down menu.
ADJUSTING THE Y AXIS SCALE
After creating an Excel chart, you may find it necessary to adjust the scale of the Y axis. Excel
automatically sets the maximum value for the Y axis based on the data used to create the chart. The
minimum value is usually set to zero. That is usually a good thing. However, depending on the data
you are using to create the chart, setting the minimum value to zero can substantially minimize the
graphical presentation of a trend. For example, the trend shown in Figure 4.4 appears to be increasing
slightly in recent months. The presentation of this trend can be improved if the minimum value
started at 500,000. The following steps explain how to make this adjustment to the Y axis:
1. Click anywhere on the Y (value or vertical) axis on the May 2014-2016 Trend for NASDAQ
Sales Volume line chart (Stock Trend worksheet).
2. Right Click and select Format Axis. The Format Axis Pane should appear, as shown in Figure
4.5.
Note: If you do not see “Format Axis . . . on your menu, you have not right clicked in the correct spot.
Press “Escape” to turn the menu off and try again
16 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 21 ]]
Figure 4.5 Format Axis Pane
1. In the Format Axis Pane, click the input box for the “Minimum” axis option and delete the zero.
Then type the number 500000 and hit Enter. As soon as you make this change, the Y axis on the
chart adjusts.
2. Click the X in the upper right corner of the Format Axis pane to close it.
3. Save your work.
Figure 4.6 shows the change in the presentation of the trend line. Notice that with the Y axis starting
at 500,000, the trend for the NASDAQ is more pronounced. This adjustment makes it easier for the
audience to see the magnitude of the trend.
BEGINNING EXCEL 17
[[ PAGE 22 ]]
Figure 4.6 Adjusted Y Axis for the S&P 500 Chart
Skill Refresher
Adjusting the Y Axis Scale
1.
Click anywhere along the Y axis to activate it.
2.
Right Click.
(Note, you can also select the Format tab in the Chart Tools section of the ribbon.)
3.
Select Format Axis . . .
4.
In the Format Axis pane, make your changes to the Axis Options.
5.
Click in the input box next to the desired axis option and then type the new scale value.
6.
Click the Close button at the top right of the Format Axis pane to close it.
TREND COMPARISONS: LINE CHART 2
We will now create a second line chart using the data in the Stock Trend worksheet. The purpose of
this chart is to compare two trends: the change in volume for the NASDAQ and the change in the
Closing price.
Before creating the chart to compare the NASDAQ volume and sales price, it is important to review
the data in the range B4:D28 on the Stock Trend worksheet. We cannot use the volume of sales and the
closing price because the values are not comparable. That is, the closing price is in a range of $45.00
to $115.00, but the data for the volume of Sales is in a range of 684,000 to 3,711,000. If we used these
values – without making changes to the chart — we would not be able to see the closing price at all.
18 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 23 ]]
The construction of this second line chart will be similar to the first line chart. The X axis will be the
months in the range B4:D28.
1. Highlight the range B4:D28 on the Stock Trend worksheet.
2. Click the Insert tab of the ribbon.
3. Click the Line button in the Charts group of commands.
4. Click the first option from the list, which is a basic line chart.
Figure 4.6.5 shows the appearance of the line chart comparing both the volume and the closing price
before it is moved and resized. Notice that the line for the closing price (Close) appears as a straight
line at the bottom of the chart. Also, the chart is covering the data again, and the title needs to be
changed.
Figure 4.6 Trend Comparison Line Chart
1. Move the chart so the upper left corner is in the middle of cell M3.
2. Resize the chart, using the resizing handles and the ALT key, so the left side is locked to the left
Note: The line representing the closing values is flat along the bottom of the chart. This is hard to see
and not very useful as is. Fear not. We will fix that.
BEGINNING EXCEL 19
[[ PAGE 24 ]]
side of Column M, the right side is locked to the right side of Column U, the top is locked to the
top of Row 3, and the bottom is locked to the bottom of Row 17.
3. Click in the text box that says “Chart Title.” Delete the text and replace it with the following: 24
Month Trend Comparison.
Good. But, we still cannot really see the Closing Price data. It is the flat red line at the very bottom of
the chart.
1. Right click the red line across the bottom of the chart that represents the Closing Price.
2. On the menu, select Format Data Series. This will open the Format Data Series pane.
3. In the Series Options, select Secondary Axis.
Figure 4.7 Adding a Secondary Axis
Better! But, it would be nice to be able to see that the values on the right represent prices.
1. Right click the Secondary Vertical Axis. (The vertical axis on the right that goes from 0 to 140.)
2. From the menu, select Format Axis.
3. In Axis Options, select Number. (You may have to scroll down to see it.)
4. Use the Symbol list box to add the $.
5. Press the Close button to close the Format Axis pane.
6. Save your work.
20 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 25 ]]
Figure 4.8 Modifying the Secondary Axis
Figure 4.9 Final Comparison Line Chart
“INSTANT” CHART – F11
On the Stock Trend worksheet:
1. Select A4:A28.
2. Hold down the Ctrl key and select D4:D28. Figure 4.10 shows what that will look like.
BEGINNING EXCEL 21
[[ PAGE 26 ]]
Figure 4.10 Range Selection
3. Press F11. (The F11 function key is on the top row of the keyboard.) If the factory default
settings haven’t been changed, Excel will create a column chart and place it on a separate chart
sheet. (See Figure 4.11).
4. Change the name of the chart sheet by double-clicking the worksheet name Chart1. Type
Closing Prices as the new name and hit Enter.
5. Save your work.
22 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 27 ]]
Figure 4.11 Instant Chart
FREQUENCY DISTRIBUTION: COLUMN CHART 1
A column chart is commonly used to show trends over time, as long as the data are limited to
approximately twenty points or less. A common use for column charts is frequency distributions. A
frequency distribution shows the number of occurrences by established categories. For example, a
common frequency distribution used in most academic institutions is a grade distribution. A grade
distribution shows the number of students that achieve each level of a typical grading scale (A, A−, B+,
B, etc.). The Grade Distribution worksheet contains final grades for some hypothetical Excel classes.
To show the grade frequency distribution for all the Excel classes in that year, the numbers of students
appear on the Y axis and the grade categories appear on the X axis. The number of students for this
chart is in Column C. The labels for grades are in Column A. The following steps explain how to
create this chart:
1. Select the Grade Distribution worksheet.
2. Change the years in Row3 to the current academic term and year.
3. Highlight the range A3:A8 on the Grade Distribution worksheet. Column A shows the grade
categories.
4. Hold down the Crtl key.
5. Without letting go of the Ctrl key, select C3:C8
BEGINNING EXCEL 23
[[ PAGE 28 ]]
6. Click the Column button in the Charts group section on the Insert tab of the ribbon. Select the
first option in the 2-D Column section, which is the Clustered Column format.
7. Click and drag the chart so the upper left corner is in the middle of cell H2.
8. Resize the chart so the left side is locked to the left side of Column H, the right side is locked to
the right side of Column O, the top is locked to the top of Row 2, and the bottom is locked to the
bottom of Row 16.
9. If Excel displays a legend, delete it by clicking the legend one time and pressing the DELETE key
on the keyboard. Since the chart presents only one data series, the legend is not necessary.
10. Add the text Final Grades for to the chart title. The chart title should now be Final Grades for
All Excel Classes 2016/2017 (or whichever academic year you are using).
11. Click any cell location on the Grade Distribution worksheet to deactivate the chart.
12. Save your work.
Figure 4.12 shows the completed grade frequency distribution chart. By looking at the chart, you can
immediately see that the greatest number of students earned a final grade in the B+ to B− range.
Figure 4.12 Grade Frequency Distribution Chart
CREATING A CHART SHEET
The charts we have created up to this point have been added to, or embedded in, an existing
worksheet (with the exception of the Instant Chart we created using F11). Charts can also be placed
in a dedicated worksheet called a chart sheet. It is called a chart sheet because it can only contain an
Excel chart. Chart sheets are useful if you need to create several charts using the data in a single
worksheet. If you embed several charts in one worksheet, it can be cumbersome to navigate and
browse through the charts. It is easier to browse through charts when they are moved to a chart
sheet because a separate sheet tab is added to the workbook for each chart. The following steps
explain how to move the grade frequency distribution chart to a dedicated chart sheet:
24 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 29 ]]
1. Click anywhere on the Final Grades for All Excel Classes chart on the Grade Distribution
worksheet.
2. Right click on the chart. Select Move Chart . . . This opens the Move Chart Dialog box.
3. Click the New sheet option on the Move Chart dialog box. (The top option.)
4. The entry in the input box for assigning a name to the chart sheet tab should automatically be
highlighted once you click the New sheet option. Type All Excel Classes. This replaces the
generic name in the input box (see Figure 4.13).
5. Click the OK button at the bottom of the Move Chart dialog box. This adds a new chart sheet to
the workbook with the name All Excel Classes.
6. Save your work.
Why?
Column Chart vs. Bar Chart
When using charts to show frequency distributions, the difference between a column chart and a bar chart is
really a matter of preference. Both are very effective in showing frequency distributions. However, if you are
showing a trend over a period of time, a column chart is preferred over a bar chart. This is because a period of
time is typically shown horizontally, with the oldest date on the far left and the newest date on the far right.
Therefore, the descriptive categories for the chart would have to fall on the horizontal – or category axis, which is
the configuration of a column chart. On a bar chart, the descriptive categories are displayed on the vertical axis.
BEGINNING EXCEL 25
[[ PAGE 30 ]]
Figure 4.13 Moving a Chart to a Chart Sheet
Figure 4.14 shows the Final Grades for the all the Excel Classes column chart is in a separate chart
sheet. Notice the new worksheet tab added to the workbook matches the New sheet name entered
into the Move Chart dialog box. Since the chart is moved to a separate chart sheet, it no longer is
displayed in the Grade Distribution worksheet.
26 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 31 ]]
Figure 4.14 Chart Sheet Added to the Workbook
FREQUENCY COMPARISON: COLUMN CHART 2
We will create a second column chart to show a comparison between two frequency distributions.
Column B on the Grade Distribution worksheet contains data showing the number of students who
received grades within each category for the Spring Quarter. We will use a column chart to compare
the grade distribution for Spring (Column B) with the overall grade distribution for the whole year
(Column C).
However, since the number of students in the term is significantly different from the total number
of students in the year, we must calculate percentages in order to make an effective comparison. The
following steps explain how to calculate the percentages:
1. Highlight the range B9:C9 on the Grade Distribution worksheet.
2. Click the AutoSum button in the Editing group of commands on the Home tab of the ribbon.
This automatically adds SUM functions that sum the values in the range B4:B8 and C4:C8.
3. Activate cell E4 on the Grade Distribution worksheet.
4. Enter a formula that divides the value in cell B4 by the total in cell B9. Add an absolute reference
to cell B9 in the formula =B4/$B$9.
5. Copy the formula in cell E4 and paste it into the range E5:E8 using the Paste command.
Or, use the Fill Handle to copy the calculation in E4 all the way down to E8.
6. Activate cell F4 on the Grade Distribution worksheet.
BEGINNING EXCEL 27
[[ PAGE 32 ]]
7. Enter a formula that divides the value in cell C4 by the total in cell C9. Add an absolute reference
to cell C9 in the formula =C4/$C$9.
8. Copy the formula in cell F4 and paste it into the range F5:F8 using the Paste command.
Or, use the Fill Handle to copy the calculation in E4 all the way down to E8.
Figure 4.15 Completed Grade Distribution Percentages
Figure 4.15 shows the completed percentages added to the Grade Distribution worksheet.
The column chart we are going to create uses the grade categories in the range A4:A8 on the X axis
and the percentages in the range E4:F8 on the Y axis. This chart uses data that is not in a contiguous
range, so we need to use the Ctrl key to select the ranges of cells.
1. Select A3:A8, hold down the Ctrl key and select E3:F8.
2. Click the Insert tab of the ribbon.
3. Click the Column button in the Charts group of commands. Select the first option from the
drop-down list of chart formats, which is the Clustered Column.
4. Click and drag the chart so the upper left corner is in the middle of cell H2.
5. Resize the chart so the left side is locked to the left side of Column H, the right side is locked to
the right side of Column N, the top is locked to the top of Row 2, and the bottom is locked to the
bottom of Row 16.
6. Change the chart title to Grade Distribution Comparison. If you do not have a chart title, you
28 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 33 ]]
can add one. On the Design tab, select Add Chart Element. Find the Chart Title. Select the
Above Chart option from the drop-down list.
7. Save your work.
Figure 4.16 Completed Data Series for the Class Grade Distribution
Figure 4.17 shows the final appearance of the column chart. The column chart is an appropriate type
for this data because there are fewer than twenty data points and we can easily see the comparison
for each category. An audience can quickly see that the class issued fewer As compared to the college.
However, the class had more Bs and Cs compared with the college population.
BEGINNING EXCEL 29
[[ PAGE 34 ]]
Figure 4.17 Completed Grade Distribution Column Chart
Integrity Check
Too Many Bars on a Column Chart?
Although there is no specific limit for the number of bars you should use on a column chart, a general rule of thumb
is twenty bars or less. Figure 4.18 contains a total of thirty-two bars. This is considered a poor use of a column
chart because it is difficult to identify meaningful trends or comparisons. The data used to create this chart might
be better used in two or three different column charts, each with a distinct idea or message.
30 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 35 ]]
Figure 4.18 Poor Use of a Column Chart
PERCENT OF TOTAL: PIE CHART
The next chart we will demonstrate is a pie chart. A pie chart is used to show a percent of total for
a data set at a specific point in time. The data we will use to demonstrate a pie chart is related to
enrollment data for Portland Area Community Colleges for Fall of 2014. You will find that data on
the Enrollment Statistics sheet.
1. Highlight the range A2:B6 on the Enrollment Statistics worksheet.
2. Click the Insert tab of the ribbon.
3. Click the Pie button in the Charts group of commands.
4. Select the first “2-D Pie” option from the drop-down list of options.
5. To make the “slices” stand out better, “explode” the pie chart.
◦Click and hold the mouse button down in any of the slices of the pie.
◦Note that you have selection handles on all of the pie slices.
◦Without letting go of your mouse button; drag one of the slices away from the center.
◦All of the slices “explode” out from the center.
BEGINNING EXCEL 31
[[ PAGE 36 ]]
1. Click off the slices and into the white canvas to deselect the pie and select the entire chart.
2. Click and drag the pie chart so the upper left corner is in the middle of cell E2.
3. Resize the pie chart so the left side is locked to the left side of Column E, the right side is locked
to the right side of Column L, the top is locked to the top of Row 2, and the bottom is locked to
the bottom of Row 10 (see Figure 4.19).
Figure 4.19 Pie Chart Moved and Resized
1. Click the chart legend once and press the DELETE key on your keyboard. A pie chart typically
shows labels next to each slice. Therefore, the legend is not needed.
2. Right click any of the slices in the pie chart, and select Add Data Labels from the list. This will
add the values for each of the slices in the pie.
3. Now, you can right click one of the numbers and select Format Data Labels from the list. This
will open the Format Data Labels pane on the right.
4. Check the boxes for Category Name and Percentage in the Label Options section in the
Note: if you let go of the mouse button before dragging, you may only get one slice to move when you
drag it out from the center. This can be another option for displaying your data. Use the Undo button to
undo this if you want to try again.
32 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 37 ]]
Format Data Labels pane. This will add the Race/ethnicity labels as well as the percentage data
to the pie chart.
5. Uncheck the box next to the Value box. This will remove the numbers from the pie chart (see
Figure 4.20).
6. Click the Close button at the top of the Format Data Labels pane.
7. Select the data labels again (if needed). Click the Home tab of the ribbon and then click the Bold
button. This will bold the data labels on the pie chart.
8. Save your work.
Figure 4.20 Final Settings in the Format Data Labels Pane
Although there are no specific limits for the number of categories you can use on a pie chart, a good
rule of thumb is ten or less. As the number of categories exceeds ten, it becomes more difficult to
identify key categories that make up the majority of the total.
BEGINNING EXCEL 33
[[ PAGE 38 ]]
Figure 4.21 Final Enrollment Statistics Pie Chart
Skill Refresher
Inserting a Pie Chart
1.
Highlight a range of cells that contain the data you will use to create the chart.
2.
Click the Insert tab of the ribbon.
3.
Click the Pie button in the Charts group.
4.
Select a format option from the Pie Chart drop-down menu.
PERCENT OF TOTAL: STACKED COLUMN CHART
The last chart type we will demonstrate is the stacked column chart. We use a stacked column chart to
show a percent of a total . For example, the data on the Enrollment Statistics worksheet shows student
enrollment by race for several colleges. We would like to see all of the data on all of the colleges.
1. Highlight the range A2:D6 on the Enrollment Statistics worksheet.
2. Click the Insert tab of the ribbon.
3. Click the Column button in the Charts group of commands. Select the 100% Stacked Column
format option from 2-D Column section in the drop-down list (see Figure 4.22).
34 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 39 ]]
Figure 4.22 Selecting the 100% Stacked Column Chart
Figure 4.23 shows the column chart that is created after selecting the 100% Stacked Column format
option. As mentioned, the goal of this chart is to show the enrollment of students by race. However,
notice that Excel places the racial categories on the X axis. It would be more useful if the different
colleges were there instead.
BEGINNING EXCEL 35
[[ PAGE 40 ]]
Figure 4.23 Initial Construction of the 100% Stacked Column Chart
The reason that Excel organized the data this way is that there are more Race/ethnicity categories
(data in column A) than there are colleges (data in row 2). Not a bad guess. But, not what we wanted
in this case.
The remaining steps explain how to correct this problem and complete the chart:
1. Click the Switch Row/Column button in the Design tab on the Chart Tools section of the
ribbon. This reverses the legend and current X axis categories.
Figure 4.24 Switch Row/
Column.
2. Click and drag the chart so the upper left corner is in the middle of cell E12.
3. Resize the chart so the left side is locked to the left side of Column E, the right side is locked to
36 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 41 ]]
the right side of Column N, the top is locked to the top of Row 12, and the bottom is locked to
the bottom of Row 30.
4. Click the legend one time and press the DELETE key on your keyboard.
5. Add a Data Table. This is another way of displaying a legend for a column chart along with the
numerical values that make up each component.
◦In earlier versions of Excel, find the Labels group of commands and select the Show Data
Table with Legend Keys option from the drop-down menu.
◦In Excel 2016, find the Add Chart Element tool on the Design tab, select Data Table With
Legend Keys
6. Change the Chart Title to Enrollment by Race.
◦If there is no chart title, you will need to add one using the Add Chart Element tool on
the Design tab.
7. Save your work.
Figure 4.25 shows the final stacked column chart. Notice the similarities and differences in the
enrollment at the local community colleges.
Figure 4.25 Final 100% Stacked Column Chart
BEGINNING EXCEL 37
[[ PAGE 42 ]]
Skill Refresher:
Inserting a Stacked Column Chart
1.
Highlight a range of cells that contain data that will be used to create the chart.
2.
Click the Insert tab of the ribbon.
3.
Click the Column button in the Charts group.
4.
Select the Stacked Column format option from the Column Chart drop-down menu to show the values of
each category on the Y axis. Select the 100% Stacked Column option to show the percent of total for each
category on the Y axis.
Key Takeaways
•
Identifying the message you wish to convey to an audience is a critical first step in creating an Excel chart.
•
Both a column chart and a line chart can be used to present a trend over a period of time. However, a line
chart is preferred over a column chart when presenting data over long periods of time.
•
The number of bars on a column chart should be limited to approximately twenty bars or less.
•
When creating a chart to compare trends, the values for each data series must be within a reasonable range.
If there is a wide variance between the values in the two data series (two times or more), the percent change
should be calculated with respect to the first data point for each series.
•
When working with frequency distributions, the use of a column chart or a bar chart is a matter of
preference. However, a column chart is preferred when working with a trend over a period of time.
•
A pie chart is used to present the percent of total for a data set.
•
A stacked column chart is used to show how a percent total changes over time.
ATTRIBUTION
Adapted by Noreen Brown from How to Use Microsoft Excel: The Careers in Practice Series, adapted
by The Saylor Foundation without attribution as requested by the work’s original creator or
licensee, and licensed under CC BY-NC-SA 3.0.
38 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 43 ]]
4.2 FORMATTING CHARTS
Learning Objectives
1.
Apply formatting commands to the X and Y axes.
2.
Enhance the visual appearance of the chart title and chart legend by using various formatting techniques.
3.
Assign titles to the X and Y axes that clarify labels and numeric values for the reader.
4.
Apply labels and formatting techniques to the data series in the plot area of a chart.
5.
Apply formatting commands to the chart area and the plot area of a chart.
6.
Employ series lines and annotations to enhance trends and provide additional information on a chart.
You can use a variety of formatting techniques to enhance the appearance of a chart once you have
created it. Formatting commands are applied to a chart for the same reason they are applied to a
worksheet: they make the chart easier to read. However, formatting techniques also help you qualify
and explain the data in a chart. For example, you can add footnotes explaining the data source as
well as notes that clarify the type of numbers being presented (i.e., if the numbers in a chart are
truncated, you can state whether they are in thousands, millions, etc.). These notes are also helpful
in answering questions if you are using charts in a live presentation. We will demonstrate these
formatting techniques using the column chart and stacked column chart from the previous section.
X AND Y AXIS FORMATS
There are numerous formatting commands we can apply to the X and Y axes of a chart. Although
adjusting the font size, style, and color are common, many more options are available through the
Format Axis pane. The following steps demonstrate a few of these formatting techniques on the
Grade Distribution Comparison chart:
1. Switch to the Grade Distribution worksheet and click anywhere along the X axis (horizontal
axis) of the Grade Distribution Comparison chart.
2. Right click and select Font.
3. Change the font to Arial, the Font Style to Bold, and the Size to 11 (see Figure 4.26).
BEGINNING EXCEL 39
[[ PAGE 44 ]]
Figure 4.26 Font Dialog Box
4. Click anywhere along the Y axis to activate it and repeat steps 2 and 3.
5. Click on the chart title and repeat steps 2 and 3, but set the Size to 14.
6. The final appearance of the axes is shown in Figure 4.27 Formatted X & Y Axes.
40 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 45 ]]
Figure 4.27 Formatted X and Y Axes
Next we want to make some changes to the percentage numbers on the Y (vertical) axis.
1. Right click the vertical (value) axis. Select Format Axis. This opens the Format Axis pane.
2. Click Number from the list of options. The commands in this section of the Format Axis pane
are used to format numbers that appear on the selected axis of the chart.
3. Click in the Decimal places input box and change the value to 1.
4. Select Axis Options. Change the Minimum Bound to .05 to make the differences in the
columns more dramatic. The Format Axis pane should match Figure 4.28.
5. Click the Close button at the top of the Format Axis pane.
6. Save your work.
BEGINNING EXCEL 41
[[ PAGE 46 ]]
Figure 4.28 Format Axis Pane changes
Note: Experiment! You can also change font styling using shortcut keys and the buttons on the Home
tab.
42 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 47 ]]
Skill Refresher
Formatting the X and Y Axes
1.
Click anywhere along the X or Y axis to activate it.
2.
Click either the Home tab or Design tab of the ribbon.
3.
Select any of the available formatting commands in these tabs.
Skill Refresher
X and Y Axis Number Formats
1.
Click anywhere along the X or Y axis to activate it.
2.
Click the Layout tab in the Chart Tools section of the ribbon.
3.
Click the Format Selection button in the Current Selection group of commands.
4.
Click Number from the list of options on the left side of the Format Axis dialog box.
5.
Select a number format and set decimal places on the right side of the Format Axis dialog box.
6.
Click the Close button in the Format Axis pane.
CHART LEGEND AND TITLE FORMATS
The next items we will format on the Grade Distribution Comparison chart are the chart legend and
title. Similar to the how we formatted the X and Y axes, we can format these items by activating them
and using the formatting commands in the Home tab or the Format pane. The following steps explain
how to add these formats:
1. Right click the legend on the Grade Distribution Comparison chart and select Format Legend.
2. Select Right in the Legend Position options. Close the Format Legend pane.
3. Move the legend by placing your cursor – shaped like a little plus sign with four arrows – on the
edge of the selection box. Click and drag the legend so the top of the legend aligns with the 35%
line next to the plot area (see Figure 4.29).
BEGINNING EXCEL 43
[[ PAGE 48 ]]
Figure 4.29 Moving the Legend
1. While the legend is still selected, change the font style in the Home tab of the ribbon to Arial.
2. Change the font size to 12 points.
3. Click the bold and italics commands in the Home tab of the ribbon.
4. Click and drag the left sizing handle so the legend is against the plot area (see Figure 4.30).
44 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 49 ]]
Figure 4.30 Legend Formatted and Resized
1. Click the chart title to activate it.
2. Right click on the chart title and select Format Chart Title to open the Format Chart Title
pane.
3. Under Title Options , in the Effects group (the option in the middle) give your title one of the
Preset shadows. Change the color, if you like.
4. Close the Format Chart Title pane.
5. Save your work.
BEGINNING EXCEL 45
[[ PAGE 50 ]]
Figure 4.31 Format Chart Title Pane
Skill Refresher
Formatting the Chart Legend
1.
Click the Legend to activate it.
2.
Click either the Home tab or right click to activate the appropriate formatting pane.
3.
Select any of the available formatting commands.
4.
Click and drag the legend to move it.
5.
Click and drag any of the sizing handles to adjust the size of the legend.
Skill Refresher
Formatting the Chart Title
46 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 51 ]]
1.
Click anywhere on the chart title.
2.
Click either the Home tab or right click to activate the appropriate formatting pane.
3.
Select any of the available formatting commands.
X AND Y AXIS TITLES
Titles for the X and Y axes are necessary for defining the numbers and categories presented on a
chart. For example, by looking at the Grade Distribution Comparison chart, it is not clear what the
percentages along the Y axis represent. The following steps explain how to add titles to the X and Y
axes to define these numbers and categories:
1. Click anywhere on the Grade Distribution Comparison chart in the Grade Distribution
worksheet to activate it.
2. On the Design tab on the ribbon select the Add Chart Element button, then Axis Titles, then
Primary Vertical. (See Figure 4.32)
Figure 4.32 Selecting a Title for the Y Axis
3. Using the Home ribbon, change the font of the axis title to Arial, Bold, size 11.
4. Click in the beginning of the Y axis title and delete the generic title. Type Percent of Enrolled
Excel Students.(see Figure 4.33).
BEGINNING EXCEL 47
[[ PAGE 52 ]]
Figure 4.33 Adding and Formatting the Y Axis Title
Next we will add the title for the X axis.
1. On the Design tab select the Add Chart Element button, then Axis Titles, then Primary
Horizontal.
2. Using the Home ribbon, change the font of the axis title to Arial, Bold, size 11.
3. Click in the beginning of the X axis title and delete the generic title. Type Final Course Grade.
Figure 4.34 shows the added titles for the X and Y axes. The titles provide definitions for the
grade categories along the X axis as well as the percentages on the Y axis.
4. Save your work.
48 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 53 ]]
Figure 4.34 X and Y Axis Titles Added
Skill Refresher
X and Y Axis Titles
1.
On the Design tab select the Add Chart Element button.
2.
Click anywhere on the chart to activate it.
3.
Select one of the options from the second drop-down list.
4.
Click in the axis title to remove the generic title and type a new title.
DATA SERIES LABELS AND FORMATS
Adding labels to the data series of a chart is a key formatting feature. A data series is the item
that is being displayed graphically on a chart. For example, the blue bars on the Grade Distribution
BEGINNING EXCEL 49
[[ PAGE 54 ]]
Comparison chart represent one data series. We can add labels at the end of each bar to show the
exact percentage the bar represents. In addition, we can add other formatting enhancements to the
data series, such as changing the color of the bars or adding an effect. The following steps explain how
to add these labels and formats to the chart:
1. Click on any of the the red bars representing the All Excel Classes data series on the Grade
Distribution Comparison chart in the Grade Distribution worksheet. Clicking one bar
automatically activates all bars in the data series. If you click a bar a second time, only that bar is
activated.
2. Right click and select Format Data Series to open up the Format Data Series pane.
3. Click the Fill and Line (paint bucket) button to bring up the Fill and Border group of
commands.
4. Click the word Fill (if needed) to expand the list of Fill options.
5. Select Pattern Fill. Then select 30% (fifth column, top row). Changing your fill pattern to a
pattern makes it easier to distinguish between the data series when you print or view your chart
in black and white. While you are there, make changes to the fill by experimenting with different
foreground and background colors.
6. Close the Format Data Series pane.
50 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 55 ]]
Figure 4.35 Changing the Fill of a Data Series
Now we are going to add the Data Labels at the end of the columns.
1. Be sure that your entire chart is selected, not just one of the data series. Click the Design tab in
the Chart Tools section of the ribbon.
2. On the Design tab select the Add Chart Element button, then Data Labels, then Outside
End (see Figure 4.36.)
3. Click on one of the Data Labels. Note that all of the data labels for that data series are selected.
4. Using the Home ribbon, change the font to Arial, Bold, size 9.
5. Click on one of the data labels for the other data series. Format those data labels as Arial, Bold,
size 9 as well.
6. Save your work.
BEGINNING EXCEL 51
[[ PAGE 56 ]]
Figure 4.36 Adding Labels to a Data Series
Figure 4.37 shows the Grade Distribution Comparison chart with the completed formatting
adjustments and labels added to the data series. Note that we can move each individual data label. This
might be necessary if two data labels overlap or if a data label falls in the middle of a grid line. To move
an individual data label, click it twice, then click and drag.
52 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 57 ]]
Figure 4.37 Completed Formatting Adjustments for the Data Series
Skill Refresher:
Adding Data Labels
1.
Click anywhere on the chart to activate it.
2.
Click the Design tab in the Chart Tools section of the ribbon.
3.
Click the Add Chart Element in the Chart Layout group.
4.
Then, select Data Labels
5.
Select one of the preset positions from the drop-down list.
BEGINNING EXCEL 53
[[ PAGE 58 ]]
Skill Refresher
Formatting a Data Series
1.
Click any bar or line for a data series.
2.
Right click to activate the Format Data Series pane.
3.
Use the formatting tools in the pane to make changes to the data series.
ADDING SERIES LINES AND ANNOTATIONS TO A CHART
The last formatting features we will demonstrate are adding series lines and annotations to a chart.
To demonstrate these skills, we will use the Change in Enrollment Statistics Spend Source stacked
column chart. Series lines are commonly used in stacked column charts to show the change from one
stack to the next. Annotations are useful for clarifying the data presented in a chart or for identifying
data sources. In addition to demonstrating these skills, we will review several of the formatting skills
that were covered in this section. The following steps include the skills review as well as the new
formatting features:
1. Locate the Enrollment by Race stacked column chart on the Enrollment Statistics worksheet.
Activate the chart by clicking anywhere inside the chart perimeter.
2. Move the chart to a separate chart sheet by clicking the Move Chart button in the Design tab of
the ribbon. Type the following in the New sheet input box: Enrollment by Race Chart. Click
the OK button.
3. Click anywhere on the data table (on the x axis) to activate it. Using the Home ribbon, change
the font to Arial, Bold, size 12.
4. Activate the Y axis and apply the same formatting adjustments as stated in step 3.
5. Add a Y axis title using Add Chart Elements – Axis Titles – then More Axis Title Options.
6. In the Format Axis Title pane change the fill color and border to colors of your choice.
7. Then, using the Home tab of the ribbon, change the font to Arial, Bold, size 14.
8. Change the text of the Y axis title to Percent Enrollment by Race.
9. Check the horizontal axis to see if this process created an extra axis title there. If it did, delete it.
10. Activate the title of the chart by clicking it once. The Format Chart Title pane should be open.
If not, right click the Chart title and select Format Chart Title from the menu. Change
the fill and border to match your vertical Axis label.
11. Then, using the Home tab of the ribbon, change the font of the chart title to Arial, Bold, size 20.
12. Close the Formatting pane.
13. Click the Add Chart Elements tool (Design tab), then Lines, then Series Lines.
This adds lines to the chart, connecting each data series between the three stacks (see Figure
4.38).
54 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 59 ]]
Figure 4.38 Selecting the Series Lines Option
1. Right click on any of the series lines added to the chart. Clicking one line will activate all lines
on the chart. (If the Format Pane is open, you will not need to right click. Just left click on any of
the series lines to change the format pane to Format Series Lines)
2. Select Format Series Lines. This will open the Format Series Lines pane.
3. Change the width to 2.25.
4. Close the Format Series Lines pane.
Figure 4.39 shows the appearance of the chart with the series lines connecting the two stacks. This
formatting enhancement is common for stacked column charts. The lines help focus the audience’s
attention to changes in the percent of total trend.
BEGINNING EXCEL 55
[[ PAGE 60 ]]
Figure 4.39 Series Lines Added to the Stacked Column Chart
Our chart demonstrates the percentage differences in enrollment between the community colleges.
But, it would be handy to know the total Enrollment at each of the colleges. To display that, we will
add text boxes above each column. To start with, we need to make room for the text boxes.
1. Select the Plot Area. Place your cursor on the top center handle of the Plot Area and drag down
about ½ inch.
Figure 4.40 Resizing the Plot Area
ADD TEXT BOXES TO INCLUDE ADDITIONAL INFORMATION IN THE CHART.
1. Click the Text Box button in the Text group on the Insert tab of the ribbon (see Figure 4.41).
2. Place the mouse pointer on the left edge of the chart area approximately one-quarter inch from
56 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 61 ]]
the top. Click and drag a rectangle approximately one and a half inches wide and one-quarter
inch high (see Figure 4.41). Don’t worry if it’s not exact – you can move and resize text boxes at
any time.
3. Type Total Enrollment. This tells the audience the size of each school.
4. Select all of the text in the text box. (You can either highlight the text or click on the border of
the text box once to select all of the text). Using the Home tab of the ribbon, change the font to
Arial, size 14.
5. Repeat the process to add and format text boxes above each column. You can try to copy and
paste the text boxes if you would like to save time.
6. In each text box, type the Total Enrollment for each school:
◦Mt Hood – 9,276
◦Portland – 30,929
◦Clackamas – 7,302
7. Save your work.
Figure 4.41 Completed Stacked Column Chart
BEGINNING EXCEL 57
[[ PAGE 62 ]]
Skill Refresher
Adding Series Lines
1.
Click anywhere on the chart area.
2.
Click the Layout tab of the ribbon.
3.
Click the Lines button in the Analysis group of commands.
4.
Click the Series Lines option from the drop-down list.
Skill Refresher:
Adding Annotations
1.
Click anywhere on the chart area.
2.
Click the Insert tab of the ribbon.
3.
Click the Text Box button in the Text group of commands.
4.
Click and drag the size of the text box needed on the chart.
5.
Apply any desired format changes from the Home tab of the ribbon.
6.
Type the desired text.
Integrity Check
Annotations and Axis Titles
Although adding annotations and axis titles can be a tedious process, doing so maintains a high level of integrity for
your charts. People can misinterpret the message being conveyed by the chart if they make inaccurate assumptions
about the values displayed. Axis titles and annotations help prevent readers from making false assumptions and
ensure that readers see the most accurate representation of the message being conveyed by the chart.
58 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 63 ]]
Key Takeaways
•
Applying appropriate formatting techniques is critical for making a chart easier to read.
•
Many formatting commands in the Home tab of the ribbon can be applied to a chart.
•
To change the number format for a data label, you must use the Number section in the Format Data Labels
dialog box. You cannot use the Number format commands in the Home tab of the ribbon.
•
To change the number format for the values on the Y axis, and the X axis in the case of a scatter chart, you
must use the Number section of the Format Axis dialog box. You cannot use the Number format commands
in the Home tab of the ribbon.
•
Axis titles and annotations help prevent false assumptions from being made and ensure that the reader sees
the most accurate representation of the information presented on a chart.
ATTRIBUTION
Adapted by Noreen Brown from How to Use Microsoft Excel: The Careers in Practice Series, adapted
by The Saylor Foundation without attribution as requested by the work’s original creator or
licensee, and licensed under CC BY-NC-SA 3.0.
BEGINNING EXCEL 59
[[ PAGE 64 ]]
4.3 USING CHARTS WITH MICROSOFT® WORD® AND MICROSOFT®
POWERPOINT®
Learning Objectives
1.
Learn how to paste an image of an Excel chart into a Word document.
2.
Learn how to paste a link to an Excel chart into a PowerPoint slide.
Charts that are created in Excel are commonly used in Microsoft Word documents or for
presentations that use Microsoft PowerPoint slides. Excel provides options for pasting an image of a
chart into either a Word document or a PowerPoint slide. You can also establish a link to your Excel
charts so that if you change the data in your Excel file, it is automatically reflected in your Word or
PowerPoint files. We will demonstrate both methods in this section.
PASTING A CHART IMAGE INTO WORD
For this exercise you will need two files:
The Excel spreadsheet you have been working with in this chapter — Ch4 Charting.
The Word document – Ch4 Diversity
Excel charts can be valuable tools for explaining quantitative data in a written report. Reports that
address business plans, public policies, budgets, and so on all involve quantitative data. For this
example, we will assume that the Change in Enrollment Statistics Spend Source stacked column chart
(see Figure 4.44) is being used in a student’s written report. The following steps demonstrate how to
paste an image, or picture, of this chart into a Word document:
1. Open Ch4 Diversity. Save it as Ch4 Diversity in Enrollment in Community Colleges
2. Click below the figure heading in the Word document that reads: Figure 1: Enrollment by
Race.
The image of the stacked column chart will be placed below this heading.
3. Open your Excel file — Ch4 Charting. Activate the Enrollment by Race chart in the Enrollment
by Race chart sheet.
4. Click the down arrow on the Copy button in the Home tab of the ribbon. Select Copy as
Picture
60 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 65 ]]
5. Select OK — Accepting the Copy Pictures defaults:
◦As shown on Screen
◦Picture
6. Go back to the Ch4 Diversity in Enrollment in Community Colleges Word document by clicking the
file in the taskbar.
7. Click the Paste button in the Home tab of the ribbon. Or, Press Crtl V.
Figure 4.42 Paste Picture in Word
Oh no!! The picture is so big that it falls on to the next page. We will need to change its size.
1. Click anywhere on the picture of the chart to activate it.
2. Click the Format tab under the Picture Tools section of the ribbon (see Figure 4.43).
3. Click the down arrow on the Shape Width button in the Size group of commands. Continue to
click the down arrow until the width of the picture is 5.4.” As you reduce the width of the
picture, the height is automatically reduced as well. (The height should be ~ 3.92″)
4. Center the chart.
◦While the chart is selected, go ot the Home tab to the Paragraph group. Select Center.
5. Save your work.
BEGINNING EXCEL 61
[[ PAGE 66 ]]
Figure 4.43 Changing the Size of a Picture in Word
Figure 4.44 shows the final appearance of the Enrollment by Race Source chart pasted into a Word
document. It is best to use either the Shape Width or Shape Height buttons to reduce the size of
the chart. Using either button automatically reduces the height and width of the chart in proper
proportion. If you choose to use the sizing handles to resize the chart, holding the SHIFT key while
clicking and dragging on a corner sizing handle will also keep the chart in proper proportion.
62 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 67 ]]
Figure 4.44 Final Appearance of Pasting a Chart Image into
Word
Skill Refresher
Pasting a Chart Image into Word
1.
Activate an Excel chart and click the Copy button in the Home tab of the ribbon.
2.
Click on the location in the Word document where the Excel chart will be pasted.
3.
Click the down arrow of the Paste button in the Home tab of the ribbon.
4.
Click the Picture option from the drop-down list.
5.
Click the Format tab in the Picture Tools section of the ribbon.
6.
Resize the picture by clicking the up or down arrow on the Shape Width or Shape Height buttons.
PASTING A LINKED CHART IMAGE INTO POWERPOINT
For this exercise you will need two files:
The Excel spreadsheet you have been working with in this chapter — Ch4 Charting.
The PowerPoint document – CH4 Diversity.
Microsoft PowerPoint is perhaps the most commonly used tool for delivering live presentations. The
charts used in a live presentation are critical for efficiently delivering your ideas to an audience.
Similar to written documents, a wide range of presentations may require the explanation of
BEGINNING EXCEL 63
[[ PAGE 68 ]]
quantitative data. This demonstration includes a PowerPoint slide that could be used in a
presentation. We will paste the Enrollment by Race chart into this PowerPoint slide. However, instead
of pasting an image, as demonstrated in the Word document, we will establish a link to the Excel file.
As a result, if we change the chart in the Excel file, the change will be reflected in the PowerPoint file.
The following steps explain how to accomplish this:
Open Ch4 Diversity.pptx. Save it as Ch4 Open the Diversity in Enrollment in Community Colleges.
Open Ch4 Charting.
1. Open your Excel file — Ch4 Charting. Activate the Enrollment by Race chart in the Enrollment
by Race chart sheet.
2. Click the down arrow on the Copy button in the Home tab of the ribbon. Select Copy (Not
Copy as Picture.)
3. Go back to the Ch4 Open the Diversity in Enrollment in Community Colleges file by clicking the file
in the taskbar.
4. Navigate to Slide 6 – Diversity in Enrollment Click on the outside edge of the empty prompt
box on the right.
5. Click the down arrow below the Paste button in the Home tab of the ribbon in the PowerPoint
file.
6. Select the Keep Source Formatting & Link Data option from the drop-down list (see Figure
4.45). This pastes an image of the Excel chart into the PowerPoint slide. In addition, a link is
created so that any changes made to the chart appear on the PowerPoint slide.
Figure 4.45 Creating a Link to an Excel Chart in PowerPoint
1. Select the outside edge of this prompt box.
2. Select the Keep Source Formatting & Link Data option
64 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 69 ]]
3. Click anywhere in the plot area of the column chart pasted into the PowerPoint slide. You will
see the same Excel Chart Tools tabs added to the ribbon (see Figure 4.46).
4. On the Design tab, select Style 8 in the Chart Style group.
Figure 4.46 Modifying an Excel Chart Pasted into a PowerPoint Slide
Paste linking this chart causes trouble with the text boxes we added. Let’s delete them.
1. Select each text box. Try for the outside edge of the text box. Press the delete key on your
keyboard.
Be sure that the outline is solid. A dotted outline is visible if you are planning to edit the
contents of the text box.
2. The benefit of adding this chart to the presentation in this way is that it will automatically
update when you change the data in the linked spreadsheet.
3. Return to the Ch4 Charting Data File. Select the Enrollment Statistics sheet. (The one with the
Enrollment data.) In cell D3, type: 1000.
You have just changed the number of white students at Clackamas Community College to 1000.
This isn’t true, but you want to change the data enough to see the effect in the charts.
4. Select the Enrollment by Race chart sheet. Notice how the chart has changed.
5. Return to the Diversity in Enrollment in Community Colleges PowerPoint file by clicking the
file in the taskbar.
6. On Slide6, you should see the updated chart.
7. If the chart has not changed; be sure that your chart is selected, click the Design tab in the Chart
Tools section of the ribbon. Click the Refresh Data button (see Figure 4.47). The change made
in the Excel workbook is now reflected on the PowerPoint slide.
8. If that still doesn’t work, you may have created a “normal” link — instead of a Paste Link.
Delete the chart and follow these steps again. Start from the beginning of this section.
BEGINNING EXCEL 65
[[ PAGE 70 ]]
9. Save your work.
Figure 4.47 Styled and Updated Chart.
Figure 4.47 shows the appearance of the column chart after the change was made in the Enrollment
Statistics worksheet in the Excel file. Note that the Data Chart at the bottom reflects the new number,
too. The change that was made in the Excel file will appear in the PowerPoint file after clicking the
Refresh Data button.
Integrity Check
Refreshing Linked Charts in PowerPoint and Word
When creating a link to a chart in Word or PowerPoint, you must refresh the data if you make any changes in
the Excel workbook. This is especially true if you make changes in the Excel file prior to opening the Word or
PowerPoint file that contains a link to a chart. To refresh the chart, make sure it is activated, then click the Refresh
Data button in the Design tab of the ribbon. Forgetting this step can result in old or erroneous data being displayed
on the chart.
66 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 71 ]]
Skill Refresher:
Pasting a Linked Chart Image into PowerPoint
1.
Activate an Excel chart and click the Copy button in the Home tab of the ribbon.
2.
Click in the PowerPoint slide where the Excel chart will be pasted.
3.
Click the down arrow of the Paste button in the Home tab of the ribbon.
4.
Click the Keep Source Formatting & Link Data option from the drop-down list.
5.
Click the Refresh Data button in the Design tab of the ribbon to ensure any changes in the Excel file are
reflected in the chart.
Key Takeaways
•
When pasting an image of an Excel chart into a Word document or PowerPoint file, use the Picture option
from the Paste drop-down list of options – if you want the image to act as an image. You will not be able to
make any changes to the content of the picture.
•
When creating a link to a chart in Word or PowerPoint, you may need to refresh the data if you make any
changes in the originating spreadsheet. You should not use the Picture option.
ATTRIBUTION
Adapted by Noreen Brown from How to Use Microsoft Excel: The Careers in Practice Series, adapted
Integrity Check
Severed Link?
When creating a link to an Excel chart in Word or PowerPoint, you must keep the Excel workbook in its original
location on your computer or network. If you move or delete the Excel workbook, you will get an error message
when you try to update the link in your Word or PowerPoint file. You will also get an error if the Excel workbook
is saved on a network drive that your computer cannot access. These errors occur because the link to the Excel
workbook has been severed. Therefore, if you know in advance that you will be using a USB drive to pull up your
documents or presentation, move the Excel workbook to your USB drive before you establish the link in your Word
or PowerPoint file.
BEGINNING EXCEL 67
[[ PAGE 72 ]]
by The Saylor Foundation without attribution as requested by the work’s original creator or
licensee, and licensed under CC BY-NC-SA 3.0.
68 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 73 ]]
4.4 PREPARING TO PRINT
Learning Objectives
1.
Review each worksheet in a workbook in Print Preview.
2.
Modify worksheets as needed to professionally print data and charts.
In this section we will take a look at each of the worksheets created in the previous sections. Since
these worksheets contain a combination of data and charts, there are specific things to watch for if
you will be printing the sheets.
We will start by looking at each worksheet in Print Preview in Backstage View. We will then make
any changes necessary, such as changing the orientation and scaling, or moving charts around on the
worksheet. To make sure we don’t miss any worksheets, we are going to review the worksheets in the
order they appear in the tabs.
PREVIEWING CHART SHEETS FOR PRINTING
Data file: Continue with CH4 Charting.
The first worksheet, Closing Prices, is a chart sheet. This means that it does not contain any data;
remember that chart sheets just contain charts. We still need to review it in Print Preview.
1. Click on the Closing Prices worksheet tab.
2. Go to Print Preview by clicking Print in Backstage View.
3. Notice that the chart will print on the entire page, in Landscape orientation.
4. There is nothing to change. Exit Backstage View.
PRINTING WORKSHEETS WITH DATA AND CHARTS
The next worksheet (Stock Trend) has a lot of data and multiple charts. We need to print the data and
the charts, which will require some modifications of the page setup.
1. Click on the Stock Trend worksheet tab.
2. Go to Print Preview by clicking Print in Backstage View.
3. Notice that this worksheet is currently printing on seven pages.
4. As you click through each page you should make the following observations:
BEGINNING EXCEL 69
[[ PAGE 74 ]]
◦The data is split between the first and third pages.
◦The line chart starts on the first page, but part of it is also on the second page.
◦The double-line chart starts on the third page, and then finishes on the fifth page.
◦The fourth and sixth pages are blank.
◦The last page has a column of seemingly random numbers.
5. Exit Backstage View.
The first thing we are going to do is remove the numbers that are appearing on page 7. To do this,
we will hide the column where they are being stored. We are going to hide the column, instead of
deleting the numbers, in case the numbers are being utilized somewhere else in the workbook.
1. Scroll to the right on the worksheet until you find the numbers in column AH.
2. Click anywhere in column AH.
3. On the Home ribbon, click the Format button in the Cells group.
4. In the Visibility section, select Hide & Unhide then select Hide Columns (see Figure 4.64).
5. The visible column headings should now go from AG to AI.
6. Return to Print Preview in Backstage View to see the changes to the printed worksheet.
7. Notice that there are now five pages. The data and charts are still splitting across multiple
pages, but the numbers in column AH are no longer going to print.
8. Remain in Backstage View for the next steps.
Figure 4.64 Hide Columns in Format Menu
The data is still split between pages 2 and 3, and the charts are splitting oddly as well. The first step
we will try to fix these issues is to change the page orientation and scaling.
1. While still in Backstage View, change the page orientation to Landscape (use the Orientation
drop-down menu in the Settings section).
2. This puts all of the data on one sheet, but the charts are still split between multiple pages.
70 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 75 ]]
3. Change the page scaling to Fit Sheet on One Page (use the Scaling drop-down menu in the
Settings section).
4. This fits everything on one page, but it is too small to be able to read.
5. Change the page scaling back to No Scaling.
The next thing we will try is moving one, or both, of the charts. In order to move the charts, we need
to exit out of Backstage View.
1. Exit Backstage View.
2. Switch to the View ribbon and then select Page Break Preview. Your screen should look similar
to Figure 4.65. (Remember that the dotted blue lines indicate automatic page breaks.)
3. Move the 24 Month Comparison (double-line) chart closer to the top of its page.
4. Move the May 2014-2015 Trend for NASDAQ Sales Volume (line chart) so that it is under the
24 Month Comparison chart.
5. The link to the data source is still at the bottom of page 2 (in A50:A51) so you need to move it as
well. Using your preferred method, move the text from A50:A51 to M31:M32.
6. Now your screen should look similar to Figure 4.66.
Figure 4.65 Page Break Preview before moving the charts in Step 3
BEGINNING EXCEL 71
[[ PAGE 76 ]]
Figure 4.66 Page Break Preview after moving the charts and text
We don’t want the data source link text to print on its own page, but there is no room to move it onto
the same page as the charts. To fix this, we are going to remove the automatic page break between the
charts and the text in M31:M32.
1. Place your pointer on the horizontal blue dashed line (automatic page break) between the line
chart and the Data Source link text.
2. When your pointer changes to the double arrow (pointing up and down), drag the page break
down into the gray area. This removes the page break.
3. If your vertical automatic page break between columns L and M moves, drag it back between
columns L and M. This will make it a solid blue line, which will no longer adjust automatically.
4. Your screen should now look like Figure 4.67.
72 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 77 ]]
Figure 4.67 Page Break Preview after removing a page break
Now you need to do one final check of this worksheet in Print Preview.
1. Go to Print Preview and look at both pages. Page 1 should contain just the data and page 2
should have both charts and the Data Source link text.
2. Exit Backstage View and save the file.
PREVIEW REMAINING WORKSHEETS FOR PRINTING
There are four remaining worksheets to be reviewed. Some of them will need minor changes and
some will not need any changes. You will need to preview each one and then make the specified
changes. In the following steps you will preview and modify the next three worksheets.
1. All Excel Classes – this is a chart sheet, so it should not need any changes.
2. Grade Distribution – the chart is split across two pages. Fix this by changing the orientation
(Landscape) and scaling (Fit Sheet on One Page).
3. Enrollment by Race Chart – this is a chart sheet, so it should not need any changes.
PRINTING A CHART ONLY
Sometimes you might have a worksheet that has data and a chart, but you only want the chart to print.
That is the case with the Enrollment Statistics worksheet.
1. Switch to the Enrollment Statistics worksheet.
2. Select the chart.
3. Go to Print Preview. Only the chart is printing. (If it shows the data printing along with the chart,
exit Backstage View and be sure to select just the chart on the worksheet.)
4. If needed, change the orientation to Landscape. This orientation looks better when printing just
a chart.
BEGINNING EXCEL 73
[[ PAGE 78 ]]
5. Exit Backstage View.
HIDING A WORKSHEET
You have actually decided that you do not want the Enrollment by Race Chart sheet to be visible at
all, but you do not want to delete it. We are going to hide it from anyone looking at the workbook.
1. Right-click on the Enrollment by Race Chart tab.
2. Select Hide from the menu that appears. The Enrollment by Race Chart sheet should no longer
be visible.
3. Save the CH4 Charting workbook.
4. Compare your work with the self-check answer key (found in the Course Files link) and then
submit the CH4 Charting workbook as directed by your instructor.
If you want to unhide a worksheet, right-click on any other worksheet tab and select Unhide from the
menu. A list of hidden worksheets will be displayed. Select the one you want and click OK.
ATTRIBUTION
“4.4 Preparing to Print” by Julie Romey, Portland Community College is licensed under CC BY 4.0
74 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 79 ]]
4.5 CHAPTER PRACTICE
To assess your understanding of the material covered in the chapter, please complete the following
assignments.
Although Excel is primarily used in business and scientific applications, you will find it useful in other
areas of study as well. In these exercises we will use Excel to create charts using historical, health, and
social justice data.
CHARTING HISTORICAL DATA (COMPREHENSIVE REVIEW)
Download Data File: PR4 Data
Excel is an excellent tool for helping to display historical date. In this exercise we will be examining
ways to display information on minimum mage data and life expectancy.
TASK1 – NATIONAL MINIMUM WAGE IN THE US – 1960-2014
Since the beginning of the previous century, the United States has set a minimum wage, in order to set
a “floor” beneath which wages cannot fall. Most states have set their own minimum wages, but none
are lower than the national minimum wage. To learn more about the national minimum wage, look
here: https://en.wikipedia.org/wiki/Minimum_wage_in_the_United_States
1. Open the file named PR4 Data and then Save As PR4 Historical Data.
2. On the Minimum Wage worksheet, select the range B4:C60
3. Select the Insert tab, then the Recommended Chart tool in the Charts group.
Recommended Charts allows users to first see how selected data would be represented on a
variety of chart types before committing to a particular type of chart. Being able to see your data
as it would look in a variety of charts helps you select the kind of chart that best matches your
date.
It does a particularly good job when you want to use dates or years as labels. Sometimes, Excel
gets confused and thinks that dates are part of the data – instead of labels.
4. Select the first Line chart. Press OK.
5. Your line chart is embedded in the Minimum Wage worksheet.
6. Make sure that the upper left corner of your chart is in the upper left corner of E4. The lower
right corner is in the lower right corner of M20.
7. Adjusting the chart title: Click the chart title once. Then click in front of the first letter. You
should see a blinking cursor in front of the letter. This allows you to modify the title of the chart.
BEGINNING EXCEL 75
[[ PAGE 80 ]]
8. Type the following in front of the first letter in the chart title: US National
9. While your chart is still selected, select the Design tab. You will find the Chart Styles group in
the middle of the ribbon. If necessary, press the More button to see the available styles.
10. Float your cursor over the available styles so you can see how they will affect your chart. Select
Style 4.
11. The years across the X (category) axis are a little hard to read.
Select the labels. When you have them selected, you will see a box surrounding the list of years.
On the Home tab, in the Alignment Group, select the Orientation tool. Select Angle Counter
Clockwise.
12. Prepare the Minimum Wage worksheet for printing by changing the scaling to Fit Sheet on
One Page.
TASK2 – OREGON: PROJECTED LIFE EXPECTANCY AT BIRTH
In the past 40 years, between 1970 and 2010, life expectancy for Oregon men improved by 8.7 years
and for women by 5.5 years. Oregon’s life expectancy has remained slightly higher than the U.S.
average. The life expectancy will continue to improve for both men and women. However, the gain
for men has been outpacing the gain for women. Consequently, the difference between men’s and
women’s life expectancies has continued to shrink.
https://www.oregon.gov/das/OEA/Documents/OR_pop_trend2012.pdf
1. On the Life Expectancy sheet, select A5:B11
2. Press F11
3. This creates a column chart, and puts it on a separate sheet.
4. Double click the chart sheet tab, change the name to Men.
5. Take a good look at this chart. It is not what we were expecting. Excel has made a mistake and
charted the Birth Year information as though it was data, instead of using it to label the bottom
(category) axis. That needs to be fixed. We need to tell Excel that the data in Column A are labels,
not values.
6. With the chart selected, go to the Design tab, and select the Select Data tool.
This opens the Select Data Source dialog box. The box at the top tells us the range we selected,
which looks fine.
The Legend Entries need to be corrected to fix the issue with the data series (columns). Also, the
Horizontal Axis Labels are just a series of default numbers. They need to be the range that contains
the years.
7. In the Legend Entries, click in the small box in front of Birth Year to remove the check mark.
This will remove the Birth Year as a data series on the chart.
8. In the Horizontal (Category) Axis Labels box, press the Edit button. This will open the Axis
Labels dialog box. Press the Select range button.
9. Navigate to the Life Expectancy tab and select A6:A11. After “=’Life Expectancy’!$A$6:$A$11”
is displayed in the box, press the Select Range button. Press OK.
Press OK
10. Change the chart title so that it reads: Life Expectancy for Oregon Men.
76 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 81 ]]
11. Remove the Legend from the bottom of the chart by right-clicking on it and selecting Delete.
12. Return to the Life Expectancy tab, select A5:All , C5:C11 (Select the first range, hold down the
CTRL key, select the next to select both noncontiguous ranges at the same time.
13. Repeat steps 2-11 above to create a matching chart for Life Expectancy for Oregon Women.
14. Return to the Life Expectancy tab, select A5:D11
15. Use the Recommended Charts tool to create a simple line chart.
16. Change the Chart Title to Oregon: Projected Life Expectancy at Birth.
17. The green line across the bottom of the chart represents the difference between men’s and
women’s life expectancy. It is not very helpful as it is.
Right click on the green line to open the pop up menu. Select Format Data Series. In the
Format Data Series pane, under the Series Options tab, select the radio button in front of
Secondary Axis.
18. Close the Format Data Series pane.
19. Add a text box that explains the Difference calculation. While the chart is still selected:
1. On the Insert tab, on the right side of the ribbon, find Text. Select the Text Box tool.
2. When you select it, your cursor will turn into cross hair (thin black plus sign)
3. Click once in the lower left corner of your chart. This creates a text box.
4. Type the following into the text box: Difference = Female life expectancy minus male.
Move or resize the text box if you wish.
20. Move or resize your chart so that it no longer is on top of the spreadsheet data.
21. Use the Chart Styles tools to change your chart to something a bit more dramatic.
22. Preview the Life Expectancy worksheet in Print Preview and make any necessary changes.
23. Save the PR4 Historical Data workbook.
24. Compare your work with the self-check answer key (found in the Course Files link) and then
submit the PR4 Historical Data workbook as directed by your instructor.
ATTRIBUTION
“4.5 Chapter Practice” by Noreen Brown, Portland Community College is licensed under CC BY 4.0
BEGINNING EXCEL 77
[[ PAGE 82 ]]
4.6 SCORED ASSESSMENT
CHARTING SOCIAL JUSTICE DATA (COMPREHENSIVE REVIEW)
Download Data File: SC4 Data
TASK 1 INTERNATIONAL INCARCERATION RATES
1. Open the file named SC4 Data and then Save As SC4 Social Justice.
2. On the International tab, make D20 your active cell. Put an =AVERAGE function in the cell.
3. Create a bar chart that looks like this:
Figure 4.68
1. Move and or resize it so that it does not cover any of the data.
2. In cell A25 write a brief note explaining why a bar (or column) chart is a better choice for this
data than a pie chart.
3. Set the Print Area so that everything prints, except for the explanation you added in cell A25.
4. Preview the International worksheet in Print Preview and make any changes needed to print
professionally on one page.
78 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 83 ]]
TASK 2 DISENFRANCHISEMENT RATE
Felony disenfranchisement is the exclusion from voting of people otherwise eligible to vote (known
as disfranchisement) due to conviction of a criminal offense, usually restricted to the more serious
class of crimes: felonies. Jurisdictions vary as to whether they make such disfranchisement permanent,
or restore suffrage after a person has served a sentence, or completed parole or probation. Affected
individuals suffer “collateral consequences” including loss of access to jobs, housing, and other
facilities.
Opponents have argued that such disfranchisement restricts and conflicts with principles of universal
suffrage. It can affect civic and communal participation in general.
https://en.wikipedia.org/wiki/Felony_disenfranchisement
On the Disenfranchisement rate sheet, use the Recommended Chart tool to create the following three
charts. Put each chart on its own individual sheet. (Note: Not an object in a spreadsheet.)
Chart1 — Felony Disenfranchisement Rate Washington
Figure 4.69
Chart2 — Felony Disenfranchisement Rate Oregon
BEGINNING EXCEL 79
[[ PAGE 84 ]]
Figure 4.70
Notes
This is called a Clustered column chart in the Recommended charts tool, but it is really a combo chart – with some
data displayed as columns and some data displayed as a line.
You will need to edit the Chart Title.
You may need to adjust the chart size to make it look like the illustration.
Put the chart on its own individual sheet — don’t leave it as an object on the spreadsheet.
Notes:
Take a look at both the Washington and Oregon charts. They are the same kind of chart, but your charts may look
different because the data is a bit different.
To make them more similar – make sure that the vertical axes are the same in both charts. Format the left vertical
(value) axis, so that the Maximum is 20000. Format the right vertical axis, so that the Maximum is .20.
80 NOREEN BROWN, BARBARA LAVE, JULIE ROMEY, MARY SCHATZ, DIANE SHINGLEDECKER
[[ PAGE 85 ]]
Chart3 – Comparison – Oregon and Washington
1. When you have completed all three charts, save your work. Preview the worksheet(s) in Print
Preview and make any necessary changes for professional printing.
2. Submit the SC4 Social Justice workbook as directed by your instructor.
ATTRIBUTION
“4.6 Scored Assessment” by Noreen Brown, Portland Community College is licensed under CC BY
4.0
Notes:
Be sure that you have years as labels on the horizontal axis (not 1, 2, 3 . . . )
This chart is on its own separate sheet.
BEGINNING EXCEL 81
[[ PAGE 86 ]]
[[ PAGE 87 ]]
CHAPTER 5 - TABLES
Excel workbooks are designed to store lots of information. Organizing this information so that they
display meaningful data can be challenging! Excel has many features that can help you organize
your data and find what you need efficiently. Setting up your data as a table from the onset will
allow you to sort, filter, total, and subtotal your data. In Excel, a table is a collection of data about a
particular subject stored in adjacent rows and columns. Tables can improve the look and feel of your
workbook. This chapter explores how to best set up Excel tables, how to edit them, and then how
to work with them effectively. These skills will be demonstrated in the context of a multi-sheet file
that shows national average weather for two very different cities in the United States. Weather data is
often voluminous and difficult to summarize since we collect weather data every hour of every day.
Providing meaningful summaries of such data is a useful skill to have.The skills learned with this data
can easily be transferred to data specific to your professional and personal needs.
ATTRIBUTION
Chapter 5 – Tables by Diane Shingledecker, Portland Community College is licensed under CC BY
4.0
[[ PAGE 88 ]]
[[ PAGE 89 ]]
CHAPTER 6 - MULTIPLE SHEET FILES
Excel workbooks often contain a large amount of data, and worksheets can quickly become
overwhelming.When one worksheet becomes cumbersome, data can be broken out into smaller
subsets and placed in separate worksheets within the same Excel file. Separating out spreadsheet data
into smaller pieces can lead to better data organization within a file and increase its ease of use.When
a retail company needs to track overall sales, as well as, individual store sales, it makes sense to place
each store’s sales data in a separate sheet within a file. Adding a summary sheet that sums across all
the sheets will allow for total company sales data in the same file! This chapter will show how to set
up a workbook to make multi-sheet formulas quick and easy.
Other examples of when multiple sheets make the most sense are when you are comparing regional
data, data for a salesforce and wish to evaluate individual salesperson performance along with overall
sales, and data over a period of time where sheets can be broken out by year or by month. When
comparing data across several sheets, it is essential that all the sheets are laid out in the same way.
To facilitate this, a template can be used. A template is the basic pattern for each new sheet that can
be used repeatedly to make sure each new sheet has the same setup, formatting, formulas, etc. as the
existing sheets in a file. In this chapter, we will use both pre-made, Microsoft Excel templates, as well
as, ones we will create from scratch to meet the specific needs of our work.
ATTRIBUTION
Chapter 6 – Multiple Sheet Files by Diane Shingledecker, Portland Community College is licensed
under CC BY 4.0
