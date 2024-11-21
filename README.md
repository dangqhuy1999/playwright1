Python 
  
  Reserved words
  class
    static class
    abstract class
  unittest
  Array: numpy, slicing,
  file , os, yaml 
  decorator tái sử dung mã nhiều lần 
  getter, setter
  multi inherritate
  polymophism

Hai đoạn mã mà bạn đã cung cấp có mục đích tương tự — cả hai đều định nghĩa một phương thức trừu tượng để yêu cầu các lớp con phải cung cấp triển khai cho phương thức đó. Tuy nhiên, chúng có những điểm khác biệt quan trọng:

### 1. Sử dụng Mô-đun `abc`

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass  # Không cần triển khai ở đây
```

- **Lớp cha `Animal` kế thừa từ `ABC`**: Điều này cho phép lớp `Animal` trở thành một lớp trừu tượng.
- **`@abstractmethod`**: Phương thức `speak` được đánh dấu là phương thức trừu tượng, yêu cầu bất kỳ lớp con nào kế thừa từ `Animal` phải triển khai phương thức này. Nếu không, lớp con sẽ không thể được khởi tạo.

### 2. Sử dụng `NotImplementedError`

```python
class Animal:
    def speak(self):
        raise NotImplementedError("Subclass must implement abstract method")
```

- **Lớp `Animal` không phải là lớp trừu tượng**: Trong trường hợp này, `Animal` là một lớp bình thường và phương thức `speak` chỉ ném ra một ngoại lệ nếu không được ghi đè.
- **Không yêu cầu kế thừa**: Lớp con có thể chọn không ghi đè phương thức `speak`, nhưng nếu chúng không làm như vậy và gọi `speak`, sẽ có lỗi xảy ra.

### So Sánh

- **Xác định rõ ràng**: Sử dụng mô-đun `abc` và `@abstractmethod` rõ ràng hơn trong việc yêu cầu các lớp con phải triển khai phương thức, và Python sẽ ngăn không cho bạn khởi tạo một lớp con chưa triển khai phương thức trừu tượng.
- **Khả năng khởi tạo**: Với cách thứ hai, bạn vẫn có thể tạo đối tượng từ lớp `Animal` mà không gặp lỗi, điều này có thể dẫn đến lỗi khi sử dụng phương thức chưa được triển khai.

### Kết Luận

Mặc dù cả hai cách đều hướng đến việc yêu cầu các lớp con phải cài đặt phương thức `speak`, cách sử dụng mô-đun `abc` với `@abstractmethod` là phương pháp chuẩn và an toàn hơn trong Python để định nghĩa các lớp trừu tượng. Điều này giúp đảm bảo rằng mã của bạn rõ ràng và dễ bảo trì hơn.

40/3
  13/3
    4/3
      1//3

tôi là đặng Quang Huy nhé bạn ơi ă ơ ô đ 
tôi là đặng  quang huy nhé bạn ơi
        
tôi là đặng quang huy  nè các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi cac
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi  các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi
các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi các bạn ơi 
các bạn ơi các bạn ơi tôi là huy nè tôi là huy nè tôi là huy nè tôi là huy nè 
tôi là huy nè tôi là huy nè tôi là huy nè tôi là huy nè tôi là huy nè
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi t
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi t
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi t
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi t

tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi 
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi 
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn  tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi tôi là huy nè các bạn ơi
