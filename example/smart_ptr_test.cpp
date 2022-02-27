#include "gtest/gtest.h"
#include <stdint.h>
#include <string>
#include <iostream>
#include <memory>

#include "test_case_builder.h"

using namespace std;
using namespace testing;
using namespace wfan;

#define TEST_NAME_TRACE() cout << "#---" << m_strTestName << "---" << endl
#define FINGERPRINT 0x8770
static long snTestNum = 0;


struct Packet
{
    uint32_t fingerprint;
    uint32_t sn;

    Packet(uint32_t seqNum): fingerprint(FINGERPRINT),sn(seqNum)
    { std::cout << "Create Packet::Packet " << sn <<endl;  }
    ~Packet()
    { std::cout << "Destroy Packet::~Packet " << sn << endl; fingerprint = 0;}
    uint32_t GetSN()
    { std::cout << "Packet::GetSN sn=" << sn << endl; return sn; }


};

uint32_t GetFingerprint(Packet* pPacket)
{
    std::cout << "Packet* pPacket address=" << pPacket << endl;
    uint32_t* pFingerprint = (uint32_t*)pPacket;
    printf("fingerprint=%d\n", *pFingerprint);
    return *pFingerprint;
}


class SmartPtrTest : public CBaseTestCase
{
public:
    SmartPtrTest(): m_strFeature("Smart Pointer") {

    }
    virtual ~SmartPtrTest() { }

    virtual void SetUp() {
        CBaseTestCase::SetUp();

    }
    virtual void TearDown()  {
        CBaseTestCase::TearDown();
    }

    virtual void RecordTestCase(string given, string when, string then, string scenario="", string checkpoints="") {
        string strClassName(::testing::UnitTest::GetInstance()->current_test_info()->test_case_name());
        string strFuncName(::testing::UnitTest::GetInstance()->current_test_info()->name());
        string strTestName = strClassName + "." + strFuncName;
        cout << "#---" << strTestName << "---" << given << ", " << when << ", " << then << endl;

        testing::Test::RecordProperty("feature", m_strFeature);
        testing::Test::RecordProperty("scenario", scenario.empty()?strTestName:scenario);
        testing::Test::RecordProperty("given", given);
        testing::Test::RecordProperty("when", when);
        testing::Test::RecordProperty("then", then);
        testing::Test::RecordProperty("checkpoints", checkpoints);
    }

protected:
    string m_strFeature;

};



TEST_F(SmartPtrTest, AutoPtrTest)
{
   RecordTestCase("create a pointer to auto_ptr", "out of the scope", "the pointer will be released");
  
   Packet* p0 = new Packet(++snTestNum);
   {
       auto_ptr<Packet> p1(p0);
       p1 -> GetSN();
       ASSERT_EQ(GetFingerprint(p0), FINGERPRINT);
   }
   
   ASSERT_NE(GetFingerprint(p0), FINGERPRINT);

}

TEST_F(SmartPtrTest, UniquePtrTest)
{
   RecordTestCase("create a pointer to unique_ptr", "out of the scope", "the pointer will be released");
	
    Packet* p0 = new Packet(++snTestNum);
    {
        std::unique_ptr<Packet> p1(p0);  // p1 owns Packet
        if (p1) p1->GetSN();
     
        {
            std::unique_ptr<Packet> p2(std::move(p1));  // now p2 owns Packet, p1 contain a null pointer
            ASSERT_FALSE(p1);
            ASSERT_EQ(GetFingerprint(p2.get()), FINGERPRINT);
            
            p1 = std::move(p2);  // ownership returns to p1
            cout << "destroying p2..." << endl;
        }
     
        if (p1) p1->GetSN();
    }
    ASSERT_NE(GetFingerprint(p0), FINGERPRINT);

}

TEST_F(SmartPtrTest, SharedPtrTest)
{
    RecordTestCase("create a pointer to shared_ptr", "out of the scope", "the pointer will be released");
    Packet* p0 = new Packet(++snTestNum);
    {
        std::shared_ptr<Packet> p1(p0);
        {
            std::shared_ptr<Packet> p2 = p1;
        }
    }
}

TEST_F(SmartPtrTest, WeakPtrTest)
{
    RecordTestCase("create a pointer to weak_ptr", "out of the scope", "the pointer will be released");
    Packet* p0 = new Packet(++snTestNum);
  
    std::shared_ptr<Packet> ps(p0);
    std::weak_ptr<Packet> pw = ps;

    std::cout << "sn == " << ps->GetSN() << ": ";
    if (auto spt = pw.lock()) { // Has to be copied into a shared_ptr before usage
        std::cout << spt->GetSN() << endl;
    }
    else {
        std::cout << "gw is expired"<< endl;
    }
}
