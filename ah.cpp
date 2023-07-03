/*class Solution {
public:
    int countRoutes(vector<int>& locations, int start, int finish, int fuel) {
        // The idea is to use a 2D array dp[i][f] to store the number of routes from city i to finish with f fuel left
        // We can fill the dp array from bottom to top and right to left
        // The base case is dp[finish][f] = 1 for any f, since there is only one route from finish to itself
        // The transition formula is dp[i][f] = sum(dp[j][f - |locations[i] - locations[j]|]) for all j != i and f - |locations[i] - locations[j]| >= 0
        // This means we can go from city i to any other city j that is reachable with the remaining fuel, and add up the number of routes from j to finish
        // The final answer is dp[start][fuel]
        
        int n = locations.size(); // the number of cities
        int mod = 1e9 + 7; // the modulo constant
        vector<vector<int>> dp(n, vector<int>(fuel + 1)); // the dp array
        
        // fill the base case
        for (int f = 0; f <= fuel; f++) {
            dp[finish][f] = 1;
        }
        
        // fill the rest of the dp array
        for (int f = 0; f <= fuel; f++) {
            for (int i = 0; i < n; i++) {
                if (i == finish) continue; // skip the finish city
                for (int j = 0; j < n; j++) {
                    if (i == j) continue; // skip the same city
                    int cost = abs(locations[i] - locations[j]); // the fuel cost to go from i to j
                    if (f >= cost) { // check if we have enough fuel
                        dp[i][f] = (dp[i][f] + dp[j][f - cost]) % mod; // add the number of routes from j to finish with f - cost fuel left
                    }
                }
            }
        }
        
        return dp[start][fuel]; // return the final answer
    }
};
*/

/*nput
locations =
[4,3,1]
start =
1
finish =
0
fuel =
6
Output
3
Expected
5*/

/*HINT : Since the array contains distinct integers fuel will always be spent in each move and so there can be no cycles.*/
/*HINT : Use dynamic programming to solve this problem with each state defined by the city index and fuel left.*/


class Solution {
public:
    int countRoutes(vector<int>& locations, int start, int finish, int fuel) {

        int n = locations.size();
        int mod = 1e9 + 7;
        vector<vector<int>> dp(n, vector<int>(fuel + 1));
        
        for (int f = 0; f <= fuel; f++) {
            dp[finish][f] = 1;
        }
        
        for (int f = 0; f <= fuel; f++) {
            for (int i = 0; i < n; i++) {
                if (i == finish) continue;
                for (int j = 0; j < n; j++) {
                    if (i == j) continue;
                    int cost = abs(locations[i] - locations[j]);
                    if (f >= cost) {
                        dp[i][f] = (dp[i][f] + dp[j][f - cost]) % mod;
                    }
                }
            }
        }
        
        return dp[start][fuel];


    }        
};