from typing import List

from cv2 import sort

nums = [3,2,2,3]
val = 3
expectedNums = [2,2]

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        print("aaa")
        try:
            print(nums)
            nums.remove(val)
        except:
            return nums
        
sol = Solution()
print(sol.removeElement(nums, val))