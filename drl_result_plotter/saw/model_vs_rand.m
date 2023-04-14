clear;
data = readmatrix("FOV2.csv");

% Load data
clc; close all;
episodes = data(:,2);
nb_data_points = numel(episodes);
len_raw = data(:,3);

% Moving Average
n = 10;   % filter order
len_filtered = filter(ones(n, 1)/n, 1, len_raw);

% Get bounds
bin_size = 30;
max_bound=[];
min_bound=[];

for i = 1:bin_size:nb_data_points-bin_size
    temp = len_raw(i:i+bin_size);
    max_bound(end+1) = max(temp);
    min_bound(end+1) = min(temp);
end
size_bounds = numel(max_bound);
n=2;
max_bound = filter(ones(n, 1)/n, 1, max_bound);
min_bound = filter(ones(n, 1)/n, 1, min_bound);
% Plot
figure(1); hold on;

x_ax = linspace(episodes(1), episodes(end), size_bounds);
x2 = [x_ax, fliplr(x_ax)];
inBetween = [min_bound, fliplr(max_bound)];
fill(x2, inBetween, [0, 0.506, 0.77], FaceAlpha=0.5, EdgeAlpha=0, HandleVisibility="off");

plot(episodes, len_filtered, Color=[0, 0.506, 0.77], LineWidth=1.3)
xlim([0, 500000])
xticks([0, 1e5 2e5 3e5 4e5 5e5 6e6])
xticklabels({'0', '100k','200k','300k','400k','500k','600k' })
xlabel("Episode Index")
ylabel("Average Episode Length")

% -----------------------------------------------------------------------------------------------------------------------------

data = readmatrix("RAND.csv");
episodes = data(:,2);
nb_data_points = numel(episodes);
len_raw = data(:,3);

% Moving Average
n = 3;   % filter order
len_filtered = filter(ones(n, 1)/n, 1, len_raw);

% Get bounds
bin_size = 10;
max_bound=[];
min_bound=[];

for i = 1:bin_size:nb_data_points-bin_size
    temp = len_raw(i:i+bin_size);
    max_bound(end+1) = max(temp);
    min_bound(end+1) = min(temp);
end
size_bounds = numel(max_bound);
n=2;
max_bound = filter(ones(n, 1)/n, 1, max_bound);
min_bound = filter(ones(n, 1)/n, 1, min_bound);
% Plot
figure(1); hold on;

x_ax = linspace(episodes(1), episodes(end), size_bounds);
x2 = [x_ax, fliplr(x_ax)];
inBetween = [min_bound, fliplr(max_bound)];
fill(x2, inBetween, [0.902, 0.149, 0], FaceAlpha=0.5, EdgeAlpha=0, HandleVisibility="off");

plot(episodes, len_filtered, Color=[0.902, 0.149, 0], LineWidth=1.3)
xlim([0, 500000])
xticks([0, 1e5 2e5 3e5 4e5 5e5 6e6])
xticklabels({'0', '100k','200k','300k','400k','500k','600k' })
xlabel("Episode Index")
ylabel("Average Episode Length")
legend("SAW Agent", "RAND")

grid on

print("drl_vs_rand", "-depsc")

















